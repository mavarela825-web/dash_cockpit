# inspect_callback_detail.py
import importlib, json, sys

name = "app"
try:
    mod = importlib.import_module(name)
except Exception as e:
    print("ERROR importing app:", e)
    sys.exit(1)

app = getattr(mod, "app", None)
if app is None:
    print("No 'app' object found in app.py")
    sys.exit(1)

target = "context-store.data"
cb = app.callback_map.get(target)
if cb is None:
    # try to find any callback id that contains the substring
    for k in app.callback_map:
        if "context-store" in k:
            target = k
            cb = app.callback_map[k]
            break

if cb is None:
    print("No callback found with id or substring 'context-store'")
    sys.exit(2)

print("Callback id:", target)
print("Full callback object:")
print(json.dumps(cb, indent=2, default=str))
print()
print("Outputs (raw):")
for o in cb.get("outputs", []):
    print(" -", repr(o))
print()
print("Inputs (raw):")
for i in cb.get("inputs", []):
    print(" -", repr(i))

sys.exit(0)
