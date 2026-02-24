import json
import os

DEFAULT_SETTINGS = {
    "download_dir": "xiaohongshu",
    "log_enable": True,
    "thread_count": 5,
    "proxy": ""
}

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)