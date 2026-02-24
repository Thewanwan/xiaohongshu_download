import unittest
from unittest.mock import patch

from app.core.parser import parse_note


class DummyResponse:
    def __init__(self, url, text):
        self.url = url
        self.text = text


class ParseNoteTests(unittest.TestCase):
    @patch("app.core.parser.requests.get")
    def test_parse_direct_note_url_with_https_images(self, mock_get):
        mock_get.return_value = DummyResponse(
            "https://www.xiaohongshu.com/explore/66aa22bb33cc44dd55ee66ff",
            '<meta content="https://sns-webpic-qc.xhscdn.com/abc123">',
        )

        note_id, sns, real_url = parse_note(
            "看看这个 https://www.xiaohongshu.com/explore/66aa22bb33cc44dd55ee66ff"
        )

        self.assertEqual(note_id, "66aa22bb33cc44dd55ee66ff")
        self.assertEqual(sns, ["abc123"])
        self.assertEqual(real_url, "https://www.xiaohongshu.com/explore/66aa22bb33cc44dd55ee66ff")

    @patch("app.core.parser.requests.get")
    def test_parse_share_short_link_redirect(self, mock_get):
        mock_get.return_value = DummyResponse(
            "https://www.xiaohongshu.com/explore/1234567890abcdef12345678",
            '{"noteId":"1234567890abcdef12345678","url":"https:\\/\\/sns-webpic-qc.xhscdn.com\\/img001"}',
        )

        note_id, sns, real_url = parse_note("https://xhslink.com/a/short")

        self.assertEqual(note_id, "1234567890abcdef12345678")
        self.assertEqual(sns, ["img001"])
        self.assertEqual(real_url, "https://www.xiaohongshu.com/explore/1234567890abcdef12345678")


if __name__ == "__main__":
    unittest.main()
