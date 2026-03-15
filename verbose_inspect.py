# verbose_inspect.py
import importlib, sys, json
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
        if isinstance(out, dict) and out.get("id") and "context-store" in out.get("id"):
            matches.append((cb_id, out))
print()
print("Matches for 'context-store':", len(matches))
for m in matches:
    print("  MATCH:", m)
sys.exit(0 if len(matches) == 1 else 2)
