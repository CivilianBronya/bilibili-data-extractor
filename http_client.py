import requests
from typing import Optional, Dict

class HttpClient:
    BASE_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    @staticmethod
    def get(url: str, referer: Optional[str] = None, headers: Optional[Dict] = None, **kwargs):
        """
        统一 GET 请求方法，自动附加浏览器 headers
        :param url: 请求地址
        :param referer: 可选的来源地址（防盗链需要）
        :param headers: 额外的 headers
        :param kwargs: 传递给 requests.get 的其他参数
        """
        final_headers = HttpClient.BASE_HEADERS.copy()
        if referer:
            final_headers["Referer"] = referer
        if headers:
            final_headers.update(headers)
        return requests.get(url, headers=final_headers, **kwargs)

    @staticmethod
    def post(url: str, data=None, json=None, referer: Optional[str] = None, headers: Optional[Dict] = None, **kwargs):
        # 统一 POST 请求方法
        final_headers = HttpClient.BASE_HEADERS.copy()
        if referer:
            final_headers["Referer"] = referer
        if headers:
            final_headers.update(headers)
        return requests.post(url, data=data, json=json, headers=final_headers, **kwargs)
