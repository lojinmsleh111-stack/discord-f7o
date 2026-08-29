import json
import os

COUNTER_FILE = "id_counter.json"
START_ID = 1445


def generate_id() -> str:
    # إذا الملف غير موجود، يبدأ من 1407
    if not os.path.exists(COUNTER_FILE):
        current_id = START_ID
    else:
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_id = int(data.get("last_id", START_ID - 1)) + 1
        except (json.JSONDecodeError, ValueError, TypeError):
            current_id = START_ID

    # حفظ آخر ID
    with open(COUNTER_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_id": current_id}, f, ensure_ascii=False, indent=2)

    return str(current_id)


def build_nickname(roblox_name: str, random_id: str) -> str:
    return f"WE | {roblox_name} | {random_id}"
