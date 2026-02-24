import re
import requests


def parse_note(url):
    url_match = re.search(r"https://www\.xiaohongshu\.com/[^\s]+", url)
    if not url_match:
        return None, [], None

    real_url = url_match.group(0)

    headers = {"user-agent": "Mozilla/5.0"}
    r = requests.get(real_url, headers=headers)

    match = re.search(r"/([0-9a-f]{24})", real_url)
    if not match:
        return None, [], real_url

    note_id = match.group(1)

    sns = re.findall('content="http://sns-webpic-qc.xhscdn.com/(.*?)">', r.text)

    return note_id, sns, real_url