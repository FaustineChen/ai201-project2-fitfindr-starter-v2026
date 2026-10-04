import tools
import agent
from utils.data_loader import get_example_wardrobe

# --- happy path: is the item that reached suggest_outfit the selected one? ---
received = {}
real_suggest = tools.suggest_outfit

def spy(new_item, wardrobe):
    received["id"] = new_item["id"]
    return real_suggest(new_item, wardrobe)

agent.suggest_outfit = spy  # agent.py imported the name directly, so patch it there

s = agent.run_agent("looking for a vintage graphic tee under $30", get_example_wardrobe())
print("error:", s["error"])
print("selected_item id:      ", s["selected_item"]["id"])
print("search_results[0] id:  ", s["search_results"][0]["id"])
print("reached suggest_outfit:", received["id"])
print("same item:", s["selected_item"]["id"] == s["search_results"][0]["id"] == received["id"])
print("fit card:", s["fit_card"])

agent.suggest_outfit = real_suggest

# --- empty path ---
s = agent.run_agent("designer ballgown size XXS under $5", get_example_wardrobe())
print()
print("error:", s["error"])
print("fit_card is None:", s["fit_card"] is None)
print("outfit_suggestion is None:", s["outfit_suggestion"] is None)