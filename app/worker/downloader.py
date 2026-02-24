import os
import time
import requests
import concurrent.futures
from PySide6.QtCore import QThread, Signal
from app.core.parser import parse_note
from app.config.settings import load_settings
from app.core.logger import write_log


class Worker(QThread):
    log_signal = Signal(str)
    progress_signal = Signal(int, int)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def log(self, msg):
        write_log(msg)
        self.log_signal.emit(msg)

    def download_one(self, i, sn, base, headers, proxies):
        img_url = f"http://sns-webpic-qc.xhscdn.com/{sn}"
        for _ in range(3):
            try:
                img = requests.get(img_url, headers=headers, timeout=10, proxies=proxies).content
                with open(os.path.join(base, f"{i}.jpg"), "wb") as f:
                    f.write(img)
                return True
            except:
                time.sleep(1)
        return False

    def run(self):
        try:
            settings = load_settings()

            base_root = settings.get("download_dir", "xiaohongshu")
            thread_count = settings.get("thread_count", 5)
            proxy = settings.get("proxy")

            proxies = {"http": proxy, "https": proxy} if proxy else None

            self.log(f"🚀 开始解析：{self.url}")

            note_id, sns, real_url = parse_note(self.url)

            if not note_id:
                self.log("❌ 解析失败")
                return

            total = len(sns)

            if total == 0:
                self.log("⚠️ 未发现可下载图片")
                return

            self.log(f"📦 共发现 {total} 张图片")

            base = os.path.join(base_root, note_id)
            os.makedirs(base, exist_ok=True)

            headers = {"user-agent": "Mozilla/5.0"}

            done = 0
            fail = 0

            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as pool:
                futures = [pool.submit(self.download_one, i, sn, base, headers, proxies) for i, sn in enumerate(sns, 1)]

                for f in concurrent.futures.as_completed(futures):
                    if f.result():
                        done += 1
                    else:
                        fail += 1

                    self.progress_signal.emit(done + fail, total)
                    self.log(f"LOG_UPDATE:正在下载 {done + fail} / {total}")

            self.log(f"✅ 下载完成 成功:{done} 失败:{fail}")

        except Exception as e:
            self.log(f"❌ 出错: {str(e)}")