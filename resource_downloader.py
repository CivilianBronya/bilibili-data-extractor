import os
import json
import requests
import yt_dlp
import subprocess
from http_client import HttpClient
from info_extractor import BilibiliInfoExtractor

class ResourceDownloader:
    """负责下载视频相关资源（封面、弹幕、视频、音频、metadata）"""

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download_all(self, video_info: dict):
        bvid = video_info["bvid"]
        save_dir = os.path.join(self.output_dir, bvid)
        os.makedirs(save_dir, exist_ok=True)

        # 保存 metadata.json
        self._save_metadata_json(video_info, save_dir)

        # 下载封面
        if video_info.get("cover_url"):
            self._download_cover(video_info["cover_url"], save_dir)

        # 下载弹幕
        if video_info.get("danmaku_url"):
            self._download_danmaku(video_info["danmaku_url"], save_dir, bvid)

        # 下载视频（含音频）
        self._download_video(video_info["bvid"], save_dir)

        # 提取音频mp3
        video_path = os.path.join(save_dir, "video.mp4")
        if os.path.exists(video_path):
            self._extract_mp3(video_path, save_dir)
        else:
            print(f"[Audio] 警告：找不到视频文件 {video_path}，跳过音频提取")

    def _save_metadata_json(self, video_info, save_dir):
        path = os.path.join(save_dir, "metadata.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(video_info, f, ensure_ascii=False, indent=4)
        print(f"[Metadata] metadata.json 已保存: {path}")

    def _download_cover(self, url, save_dir):
        cover_path = os.path.join(save_dir, "cover.jpg")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        with open(cover_path, "wb") as f:
            f.write(resp.content)
        print(f"[Cover] 封面已保存: {cover_path}")

    def _download_danmaku(self, danmaku_url, save_dir, bvid):
        output_path = os.path.join(save_dir, "danmaku.xml")
        resp = HttpClient.get(
            danmaku_url,
            referer=f"https://www.bilibili.com/video/{bvid}/",
            timeout=10
        )
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"[Danmaku] 弹幕已保存: {output_path}")

    def _download_video(self, bvid, save_dir):
        ydl_opts = {
            "outtmpl": os.path.join(save_dir, "video.%(ext)s"),
            "format": "bv+ba/b",
            "merge_output_format": "mp4",
            "postprocessors": [],  # 不自动提取音频，保留视频文件
            "quiet": True,
        }
        # TODO(FinNank1ng 星丶白羽莲)：url复用后续优化
        url = f"https://www.bilibili.com/video/{bvid}"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"[Video] 视频已保存: {save_dir}")

    def _extract_mp3(self, video_path, save_dir):
        mp3_path = os.path.join(save_dir, "video.mp3")
        cmd = [
            "ffmpeg",
            "-y",                   # 覆盖输出
            "-i", video_path,
            "-vn",                  # 不包含视频
            "-acodec", "libmp3lame",
            "-q:a", "2",            # 高质量音频
            mp3_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[Audio] 音频已提取: {mp3_path}")
