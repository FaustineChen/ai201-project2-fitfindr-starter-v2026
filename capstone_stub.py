#!/usr/bin/env python3
"""
A fake model server for the capstone tests.

It speaks just enough of the Gemini REST API (POST .../models/<model>:generateContent)
for generate.py to talk to it, and it fails on command:

    ok      answers normally
    503     HTTP 503 "UNAVAILABLE"
    drop    closes the connection without answering
    empty   answers 200 with an empty text
    hang    never answers (waits until the client gives up, up to HANG_LIMIT_S)

You give it a script, one behavior per call, in order. When the script runs
out, the last entry repeats:

    stub.set_script(["503", "503", "ok"])   # fail twice, then answer
    stub.set_script(["503"])                # fail every time

It is only used by capstone_eval.py. Nothing in the deployed app imports it.
"""

import json
import select
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HANG_LIMIT_S = 40  # longer than REQUEST_TIMEOUT, so the client always gives up first


class Stub:
    def __init__(self):
        self.lock = threading.Lock()
        self.script = ["ok"]
        self.calls = []  # one dict per request: n, behavior, t, cut_off_s
        self.server = None
        self.thread = None

    # ── control ──────────────────────────────────────────────────────────────

    def set_script(self, script):
        with self.lock:
            self.script = list(script)
            self.calls = []

    def start(self):
        stub = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):  # keep the terminal quiet
                pass

            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length).decode("utf-8", "replace") if length else ""
                stub._handle(self, body)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.url

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    @property
    def url(self):
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    # ── behavior ─────────────────────────────────────────────────────────────

    def _next_behavior(self):
        with self.lock:
            n = len(self.calls)
            behavior = self.script[min(n, len(self.script) - 1)]
            record = {"n": n + 1, "behavior": behavior, "t": time.monotonic(),
                      "cut_off_s": None}
            self.calls.append(record)
            return behavior, record

    def _handle(self, handler, body):
        behavior, record = self._next_behavior()

        if behavior == "503":
            payload = json.dumps({"error": {
                "code": 503, "status": "UNAVAILABLE",
                "message": "The model is overloaded. Please try again later.",
            }}).encode()
            handler.send_response(503)
            handler.send_header("Content-Type", "application/json")
            handler.send_header("Content-Length", str(len(payload)))
            handler.end_headers()
            handler.wfile.write(payload)
            return

        if behavior == "drop":
            try:
                handler.connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            handler.close_connection = True
            return

        if behavior == "hang":
            self._hang(handler, record)
            return

        text = "" if behavior == "empty" else self._answer(body)
        self._reply(handler, text)

    def _hang(self, handler, record):
        """Wait for the client to hang up, and record how long that took."""
        start = time.monotonic()
        sock = handler.connection
        while time.monotonic() - start < HANG_LIMIT_S:
            ready, _, _ = select.select([sock], [], [], 0.2)
            if ready:
                try:
                    if sock.recv(1, socket.MSG_PEEK) == b"":
                        break  # the client closed its side
                except OSError:
                    break
        record["cut_off_s"] = round(time.monotonic() - start, 2)
        handler.close_connection = True

    @staticmethod
    def _answer(prompt_json):
        if "caption" in prompt_json.lower():
            return ("Just scored this tee for $12.00 on Depop and it pairs "
                    "perfectly with my everyday jeans. Total thrift win.")
        return "Pair it with your light-wash jeans and white sneakers."

    @staticmethod
    def _reply(handler, text):
        payload = json.dumps({
            "candidates": [{
                "content": {"role": "model", "parts": [{"text": text}]},
                "finishReason": "STOP",
                "index": 0,
            }],
            "usageMetadata": {"promptTokenCount": 10, "candidatesTokenCount": 10,
                              "totalTokenCount": 20},
        }).encode()
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(payload)))
        handler.end_headers()
        handler.wfile.write(payload)


if __name__ == "__main__":
    # A quick way to see it run: python capstone_stub.py
    s = Stub()
    print("stub listening on", s.start())
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        s.stop()
