# Douyin API examples

[简体中文](README.md)

Python examples for searching Douyin videos and retrieving video details and comments through Just One API. Use them as building blocks for an **API-based Douyin scraper** or data collection workflow.

This is a third-party API client example, not an official Douyin SDK or a standalone scraper. A Just One API account, access token, and endpoint permissions are required. Requests may incur charges; check your dashboard for pricing, trial quotas, and availability. These examples cover Douyin content only, not TikTok, Douyin e-commerce, or Xingtu.

## Quick start

Python 3.10+, with no external dependencies.

```bash
git clone https://github.com/justoneapi-labs/douyin-api.git
cd douyin-api
export JUSTONEAPI_TOKEN='YOUR_TOKEN'
python3 douyin.py search 'coffee'
python3 douyin.py detail 'YOUR_VIDEO_ID'
python3 douyin.py comments 'YOUR_VIDEO_ID' --page 1
```

Keep your token out of Git, logs, and issues. Each command sends exactly one request and prints JSON to stdout. Errors produce a nonzero exit code. There are no automatic retries or collection loops.

To save a response:

```bash
mkdir -p results
python3 douyin.py search 'coffee' > results/search.json
```

`results/` is excluded from Git.

## Pagination

For search pages after page 1, pass `data.business_config.next_page.search_id` from the previous response. Stop when `data.business_config.has_more` is `0`. Inspect the real response before replacing the placeholder:

```bash
python3 douyin.py search 'coffee' --page 2 --search-id 'SEARCH_ID_FROM_PREVIOUS_RESPONSE'
```

Comments use `--page`; video details do not support pagination. The script preserves the raw `data` response. See the [API documentation](https://docs.justoneapi.com/en/) for the full response structure and optional filters.

| Command | API endpoint | Main parameters |
|---|---|---|
| `search` | `/api/douyin/search-video/v4` | `keyword`, `page`, `searchId` |
| `detail` | `/api/douyin/get-video-detail/v2` | `videoId` |
| `comments` | `/api/douyin/get-video-comment/v1` | `awemeId`, `page` |

These examples follow the published OpenAPI contract. Offline tests check request encoding, pagination validation, and error handling; they do not verify successful calls to the paid live service. Check permissions, balance, and endpoint status before manually retrying a failed request.

## Offline tests

```bash
python3 -m unittest -v
```

Tests use mock responses. They require no token and incur no API fees.

## Resources

- [Just One API](https://justoneapi.com/en/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_douyin_api&utm_content=readme_link)
- [API documentation](https://docs.justoneapi.com/en/)
- [Account dashboard](https://dashboard.justoneapi.com/en/)
- [Official Python SDK](https://github.com/justoneapi-official/justoneapi-python)

Only process data you are authorized to access and use. Remove tokens, personal information, and private response content before reporting issues.

## License

The example code is [MIT licensed](LICENSE). This license does not grant API service access or rights to collected data.
