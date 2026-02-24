import os
import datetime
from app.config.settings import load_settings

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def write_log(msg):
    settings = load_settings()

    if not settings.get("log_enable", True):
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] {msg}\n"

    with open(os.path.join(LOG_DIR, "app.log"), "a", encoding="utf-8") as f:
        f.write(line)