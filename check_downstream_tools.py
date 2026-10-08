import config
import tools
import agent
from utils.data_loader import get_example_wardrobe

config.CACHE_ENABLED = False
QUERY = "vintage graphic tee under $30"

received = {}

# 攔 call_tool：不管叫哪個 tool，只要 args 裡有 new_item 就記 id
real_call_tool = agent.call_tool

def spy_call_tool(name, args, *rest, **kwargs):
    item = args.get("new_item") if isinstance(args, dict) else None
    if item is not None:
        received[name] = item["id"]
    return real_call_tool(name, args, *rest, **kwargs)

# suggest_outfit 如果是直接呼叫（不經 call_tool），保留原本的 spy
real_suggest = tools.suggest_outfit

def spy_suggest(new_item, *args, **kwargs):
    received["suggest_outfit"] = new_item["id"]
    return real_suggest(new_item, *args, **kwargs)

agent.call_tool = spy_call_tool
agent.suggest_outfit = spy_suggest

passes = 0
for i in range(1, 6):
    received.clear()
    s = agent.run_agent(QUERY, get_example_wardrobe())
    if s["error"] or not s["search_results"]:
        print(f"try {i}: FAIL (stopped early: {s['error']})")
        continue
    ids = {
        "selected_item": s["selected_item"]["id"],
        "search_results[0]": s["search_results"][0]["id"],
        "suggest_outfit": received.get("suggest_outfit"),
        "create_fit_card": received.get("create_fit_card"),
    }
    ok = len(set(ids.values())) == 1 and None not in ids.values()
    passes += ok
    print(f"try {i}: {'PASS' if ok else 'FAIL'}  {ids}")

print(f"\n{passes}/5")

agent.call_tool = real_call_tool
agent.suggest_outfit = real_suggest