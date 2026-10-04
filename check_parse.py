from agent import parse_query

for q in [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "designer ballgown size XXS under $5",
    "one size hoodie under 40",
    "oversized graphic tee",
]:
    print(q, "->", parse_query(q))