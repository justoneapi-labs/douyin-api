import io
import json
import unittest
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse, parse_qs
from douyin import request


class ClientTests(unittest.TestCase):
    def capture(self, calls):
        def opener(url, timeout):
            calls.append((urlparse(url), timeout))
            return io.StringIO(json.dumps({"code": 0, "data": {"items": []}}))
        return opener

    def test_search_pagination_and_unicode(self):
        calls = []
        request("search", "咖啡 & 旅行", "test-token", page=2, search_id="next-id", opener=self.capture(calls))
        url, timeout = calls[0]
        self.assertEqual(url.path, "/api/douyin/search-video/v4")
        self.assertEqual(parse_qs(url.query), {"keyword": ["咖啡 & 旅行"], "token": ["test-token"], "page": ["2"], "searchId": ["next-id"]})
        self.assertEqual(timeout, 30)

    def test_distinct_video_id_parameter_names(self):
        for action, path, key in [("detail", "/api/douyin/get-video-detail/v2", "videoId"), ("comments", "/api/douyin/get-video-comment/v1", "awemeId")]:
            with self.subTest(action=action):
                calls = []
                request(action, "123", "test-token", opener=self.capture(calls))
                url = calls[0][0]
                self.assertEqual(url.path, path)
                self.assertEqual(parse_qs(url.query)[key], ["123"])

    def test_bad_inputs_never_send_a_request(self):
        def forbidden(*a, **kw):
            self.fail("Invalid input must not call a paid endpoint")
        cases = [("search", "word", "", {}), ("search", "word", "token", {"page": 2}),
                 ("comments", "123", "token", {"page": 0}), ("detail", "123", "token", {"page": 2}),
                 ("detail", "123", "token", {"search_id": "id"}), ("search", " ", "token", {})]
        for action, value, token, kwargs in cases:
            with self.subTest(action=action, kwargs=kwargs), self.assertRaises(ValueError):
                request(action, value, token, opener=forbidden, **kwargs)

    def test_transport_errors_do_not_expose_token_or_retry(self):
        for error in [HTTPError("https://example.test/?token=SECRET", 429, "SECRET", {}, None), URLError("SECRET"), TimeoutError("SECRET")]:
            calls = []
            def opener(*args, **kwargs):
                calls.append(1)
                raise error
            with self.assertRaises(RuntimeError) as caught:
                request("detail", "123", "SECRET", opener=opener)
            self.assertNotIn("SECRET", str(caught.exception))
            self.assertEqual(len(calls), 1)

    def test_invalid_and_error_responses(self):
        for body in ['not-json', '[]', '{"code": 401, "message": "SECRET"}', '{}']:
            with self.subTest(body=body), self.assertRaises(RuntimeError) as caught:
                request("detail", "123", "SECRET", opener=lambda *a, **kw: io.StringIO(body))
            self.assertNotIn("SECRET", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
