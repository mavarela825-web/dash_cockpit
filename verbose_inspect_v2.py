# verbose_inspect_v2.py
import importlib, sys, json

def out_contains_context_store(out):
    # dict with id
    if isinstance(out, dict):
        idv = out.get("id") or out.get("component_id") or out.get("componentId")
        if isinstance(idv, str) and "context-store" in idv:
            return True
    # tuple/list like (id, prop)
    if isinstance(out, (list, tuple)) and len(out) >= 1:
        first = out[0]
        if isinstance(first, str) and "context-store" in first:
            return True
    # string like "context-store.data"
    if isinstance(out, str) and "context-store" in out:
        return True
    return False

try:
    mod = importlib.import_module("app")
except Exception as e:
    print("ERROR importing app:", e)
    sys.exit(1)

app = getattr(mod, "app", None)
if app is None:
    print("No 'app' object found in app.py")
    sys.exit(1)

matches = []
print("Listing callbacks and outputs:")
for cb_id, cb in app.callback_map.items():
    outputs = cb.get("outputs", [])
    print(f"- CALLBACK: {cb_id}")
    for out in outputs:
        print("    ->", out)
        if out_contains_context_store(out):
            matches.append((cb_id, out))

print()
print("Matches for 'context-store':", len(matches))
for cb_id, out in matches:
    print("  MATCH:", cb_id, "->", out)

sys.exit(0 if len(matches) == 1 else 2)
