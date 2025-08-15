import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from http_client import HttpClient
from typing import Callable, Optional

class BilibiliInfoExtractor:
    # B站视频信息提取器，结合网页和API获取视频详细信息
    def __init__(self, log: Optional[Callable[[str], None]] = None):
        """
        :param log: 日志回调函数 log(str)，默认使用 print
        """
        print("[DEBUG] BilibiliInfoExtractor 初始化", flush=True)
        self.session = requests.Session()
        self.session.headers.update(HttpClient.BASE_HEADERS)
        self.log = log or (lambda s: print(s, flush=True))

    def get_video_info(self, bvid: str) -> dict:
        """
        视频BV号获取完整视频信息
        :param bvid: 视频BV号，如 'BV1tG4y1s72q'
        :return: dict 包含视频详情字段
        """
        print(f"[DEBUG] get_video_info 调用: {bvid}", flush=True)
        try:
            base_url = f"https://www.bilibili.com/video/{bvid}"
            resp = self.session.get(base_url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            self.log(f"[HTTP ERROR] 获取网页 {bvid} 失败: {e}")
            return {}

        try:
            soup = BeautifulSoup(resp.text, "html.parser")
            script_tag = soup.find("script", string=re.compile(r"window\.__INITIAL_STATE__"))
            if not script_tag:
                self.log(f"[WARN] 未找到 __INITIAL_STATE__ 数据: {bvid}")
                return {}

            match = re.search(r"window\.__INITIAL_STATE__=(\{.*?\});", script_tag.string)
            if not match:
                self.log(f"[WARN] 未能从脚本中提取 __INITIAL_STATE__ JSON: {bvid}")
                return {}

            initial_state = json.loads(match.group(1))
            video_data = initial_state.get("videoData", {})
            if not video_data:
                self.log(f"[WARN] 未能解析 videoData: {bvid}")
                return {}

            cid = video_data.get("cid")
        except Exception as e:
            self.log(f"[PARSE ERROR] 解析网页 {bvid} 失败: {e}")
            return {}

        # API 数据
        # TODO(FinNank1ng 星丶白羽莲)：考虑复用性整合代码，双保险也需要考虑优化，API拿不到基本信息
        try:
            api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            api_resp = self.session.get(api_url, timeout=10).json()
            api_data = api_resp.get("data", {})
        except Exception as e:
            self.log(f"[API ERROR] 获取API数据 {bvid} 失败: {e}")
            api_data = {}

        # 发布时间格式化
        pubdate_ts = api_data.get("pubdate", 0)
        try:
            publish_date = datetime.fromtimestamp(pubdate_ts).strftime("%Y-%m-%d %H:%M:%S") if pubdate_ts else "未知"
        except Exception:
            publish_date = "未知"

        # 作者简介
        video_desc = video_data.get("desc", "").strip()
        author_desc = video_desc if video_desc else "未找到作者简介"

        # 标签
        tags_list = api_data.get("tag")
        tags = None
        if tags_list and isinstance(tags_list, list):
            tags = ",".join(t.get("tag_name", "") for t in tags_list if t.get("tag_name"))
            if not tags:
                tags = None
        # TODO(FinNank1ng 星丶白羽莲): 构式结构，日后考虑优化
        if not tags:
            try:
                keywords_meta = soup.find("meta", itemprop="keywords")
                if keywords_meta and keywords_meta.has_attr("content"):
                    keywords = keywords_meta["content"].strip()
                    if keywords:
                        keyword_list = keywords.split(",")
                        title = video_data.get("title", "").strip()
                        if title in keyword_list:
                            keyword_list.remove(title)
                        if len(keyword_list) > 4:
                            keyword_list = keyword_list[:-4]
                        tags = ",".join(keyword_list) if keyword_list else "该视频没有标签"
                    else:
                        tags = "该视频没有标签"
                else:
                    tags = "该视频没有标签"
            except Exception as e:
                self.log(f"[TAG WARN] 获取标签失败: {e}")
                tags = "该视频没有标签"
        if not tags:
            tags = "该视频没有标签"

        # 返回信息
        result = {
            "bvid": bvid,
            "cid": cid,
            "title": video_data.get("title", "无标题").strip(),
            "author": video_data.get("owner", {}).get("name", "未知作者"),
            "author_id": str(video_data.get("owner", {}).get("mid", "")),
            "publish_date": publish_date,
            "duration": api_data.get("duration", 0),
            "views": api_data.get("stat", {}).get("view", 0),
            "danmaku": api_data.get("stat", {}).get("danmaku", 0),
            "likes": api_data.get("stat", {}).get("like", 0),
            "coins": api_data.get("stat", {}).get("coin", 0),
            "favorites": api_data.get("stat", {}).get("favorite", 0),
            "shares": api_data.get("stat", {}).get("share", 0),
            "video_desc": video_data.get("desc", "").strip(),
            "author_desc": author_desc,
            "tags": tags,
            "cover_url": video_data.get("pic", ""),
            "danmaku_url": f"https://comment.bilibili.com/{cid}.xml" if cid else None,
            "video_aid": str(video_data.get("aid", "")),
        }
        print(f"[DEBUG] 返回数据: {json.dumps(result, ensure_ascii=False, indent=2)}", flush=True)
        return result