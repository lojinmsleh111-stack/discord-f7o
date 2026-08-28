import random


def generate_id() -> str:
    """إيدي عشوائي من 4 أرقام."""
    return str(random.randint(1000, 9999))


def build_nickname(roblox_name: str, random_id: str) -> str:
    """بناء الاسم النهائي."""
    return f"WE | {roblox_name} | {random_id}"
