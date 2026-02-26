import json
import os

STATE_FILE = "cockpit_state.json"

DEFAULT_STATE = {
    "polarity": {
        "HTF": "N",
        "ITF": "N",
        "STF": "N",
        "Overnight": "N"
    },
    "tick_value": 0
}

def load_state():
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)
