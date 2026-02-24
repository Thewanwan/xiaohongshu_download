import re
import requests


def _extract_first_url(text):
    return re.search(r"https?://[^\s]+", text)


def _extract_note_id(candidate_text):
    match = re.search(r"/([0-9a-f]{24})(?:\?|$)", candidate_text)
    if match:
        return match.group(1)

    match = re.search(r'"noteId"\s*:\s*"([0-9a-f]{24})"', candidate_text)
    if match:
        return match.group(1)

    return None


def _extract_images(html):
    patterns = [
        r'https?://sns-webpic-qc\.xhscdn\.com/([^"\'<>\s]+)',
        r'https?:\\/\\/sns-webpic-qc\.xhscdn\.com\\/([^"\'<>\s]+)',
    ]

    seen = set()
    result = []
    for pattern in patterns:
        for sn in re.findall(pattern, html):
            cleaned = sn.replace('\\/', '/')
            if cleaned not in seen:
                seen.add(cleaned)
                result.append(cleaned)
    return result


def parse_note(url):
    url_match = _extract_first_url(url)
    if not url_match:
        return None, [], None

    origin_url = url_match.group(0)
    headers = {"user-agent": "Mozilla/5.0"}

    try:
        response = requests.get(origin_url, headers=headers, timeout=15, allow_redirects=True)
    except requests.RequestException:
        return None, [], origin_url

    real_url = response.url or origin_url
    note_id = _extract_note_id(real_url) or _extract_note_id(response.text)
    if not note_id:
        return None, [], real_url

    sns = _extract_images(response.text)

    return note_id, sns, real_url
