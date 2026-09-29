"""Douyin data collection examples using the third-party Just One API service."""
import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

ENDPOINTS = {
    "search": ("/api/douyin/search-video/v4", "keyword"),
    "detail": ("/api/douyin/get-video-detail/v2", "videoId"),
    "comments": ("/api/douyin/get-video-comment/v1", "awemeId"),
}


def request(action, value, token, *, page=1, search_id="", opener=urlopen):
    if action not in ENDPOINTS:
        raise ValueError("Unknown action.")
    if not token or not token.strip():
        raise ValueError("Set JUSTONEAPI_TOKEN before making a request.")
    if not value or not value.strip():
        raise ValueError("Provide a search keyword or video ID.")
    if page < 1:
        raise ValueError("Page must be at least 1.")
    if action == "search" and page > 1 and not search_id:
        raise ValueError("Search pages after page 1 require --search-id from the previous response.")
    if action == "detail" and page != 1:
        raise ValueError("Video details do not support pagination.")
    if search_id and action != "search":
        raise ValueError("--search-id is only valid for search.")
    path, key = ENDPOINTS[action]
    params = {"token": token, key: value}
    if action in ("search", "comments"):
        params["page"] = page
    if action == "search" and search_id:
        params["searchId"] = search_id
    # The service requires a query token. Never print this URL in logs/errors.
    url = "https://api.justoneapi.com" + path + "?" + urlencode(params)
    try:
        with opener(url, timeout=30) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}. Check your account and endpoint documentation.") from None
    except (URLError, TimeoutError, OSError):
        raise RuntimeError("Network request failed. Check connectivity before retrying manually.") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("Server returned invalid JSON.") from None
    if not isinstance(result, dict) or result.get("code") != 0:
        raise RuntimeError("API request failed. Check account permissions, balance, and endpoint status.")
    return result


def main():
    parser = argparse.ArgumentParser(description="Douyin API / 抖音API — Just One API examples")
    parser.add_argument("action", choices=ENDPOINTS)
    parser.add_argument("value", help="Search keyword, or video ID for details/comments")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--search-id", default="")
    args = parser.parse_args()
    try:
        result = request(args.action, args.value, os.environ.get("JUSTONEAPI_TOKEN", ""),
                         page=args.page, search_id=args.search_id)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
