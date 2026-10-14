# 抖音API · 抖音接口

[English](README.en.md)

使用 Python 标准库调用 Just One API，查询抖音视频搜索、视频详情和评论。适合需要通过第三方 API 构建抖音数据采集流程的开发者。

这是第三方 **API 调用与爬虫工作流示例**，不是抖音官方 SDK，也不是无需服务端 API 的独立爬虫。需要 Just One API 账户、有效 Token 和对应接口权限；调用可能收费，价格、试用额度与可用性以控制台为准。此仓库不包含 TikTok、抖音电商或星图接口。

## 快速开始

Python 3.10+，无需安装依赖。

```bash
git clone https://github.com/justoneapi-labs/douyin-api.git
cd douyin-api
# 从控制台获取 Token，在本地设置；不要提交到 Git 或贴到 Issue。
export JUSTONEAPI_TOKEN='YOUR_TOKEN'
python3 douyin.py search '咖啡'
python3 douyin.py detail 'YOUR_VIDEO_ID'
python3 douyin.py comments 'YOUR_VIDEO_ID' --page 1
```

每条命令只请求一次，JSON 结果输出到标准输出。查询失败时返回非零退出码，不自动重试或连续采集。

保存结果：

```bash
mkdir -p results
python3 douyin.py search '咖啡' > results/search.json
```

`results/` 已忽略，不会默认提交采集结果。

## 搜索翻页

第一页响应的 `data.business_config.next_page.search_id` 用作下一页的 `--search-id`；`data.business_config.has_more` 为 `0` 时停止翻页。请检查实际响应后手动传入值，不要直接运行占位符。

```bash
python3 douyin.py search '咖啡' --page 2 --search-id 'SEARCH_ID_FROM_PREVIOUS_RESPONSE'
```

评论按 `--page` 分页；详情查询不接受分页。完整参数和响应结构请查阅[接口文档](https://docs.justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_douyin_api&utm_content=readme_docs_zh)。响应 `data` 保留服务返回的原始结构，脚本不假定视频或评论字段长期不变。

## 使用的接口

| 命令 | API 路径 | 主要参数 |
|---|---|---|
| `search` | `/api/douyin/search-video/v4` | `keyword`、`page`、`searchId` |
| `detail` | `/api/douyin/get-video-detail/v2` | `videoId` |
| `comments` | `/api/douyin/get-video-comment/v1` | `awemeId`、`page` |

接口依照公开 OpenAPI 文档编写。离线测试验证参数编码、翻页约束和异常处理；不代表已经对付费线上接口做了成功调用测试。网络或服务错误不会自动重试；重试前请检查账户、余额、权限和服务状态。

## 离线测试

```bash
python3 -m unittest -v
```

测试使用模拟响应，不需要 Token，也不会产生 API 费用。

## 链接

- [Just One API](https://justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_douyin_api&utm_content=readme_link)
- [API 文档](https://docs.justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_douyin_api&utm_content=readme_docs_zh)
- [账户与接口权限](https://dashboard.justoneapi.com/zh/?utm_source=github.com&utm_medium=referral&utm_campaign=justoneapi_labs_douyin_api&utm_content=readme_dashboard_zh)
- [官方 Python SDK](https://github.com/justoneapi-official/justoneapi-python)

请仅处理你有权访问和使用的数据。提交 Issue 时请去除 Token、个人信息及不应公开的响应内容。

## License

示例代码采用 [MIT License](LICENSE)；API 服务条款及数据使用权不由此代码许可证授予。
