# inspect_callbacks.py
import importlib, sys
name = "app"
try:
    mod = importlib.import_module(name)
except Exception as e:
    print("ERROR importing module 'app':", e)
    sys.exit(1)
app = getattr(mod, "app", None)
if app is None:
    print("No 'app' object found in app.py")
    sys.exit(1)
count = 0
for cb_id, cb in app.callback_map.items():
    outputs = cb.get("outputs", [])
    for out in outputs:
        if isinstance(out, dict) and out.get("id") and "context-store" in out.get("id"):
            print("  CALLBACK:", cb_id, "->", out)
            count += 1
print("Total callbacks that output to context-store:", count)
sys.exit(0 if count == 1 else 2)
