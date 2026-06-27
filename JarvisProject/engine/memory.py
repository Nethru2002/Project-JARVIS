import json
import os

MEMORY_FILE = "user_memory.json"

def save_memory(fact_key, fact_val):
    memory = load_all_memory()
    memory[fact_key] = fact_val
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def load_all_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def get_memory_string():
    mem = load_all_memory()
    if not mem: return ""
    return "User Facts: " + ", ".join([f"{k} is {v}" for k, v in mem.items()])