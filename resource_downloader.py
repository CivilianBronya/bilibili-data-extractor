import os
import json
import requests
import yt_dlp
import subprocess
import threading
import gc
from http_client import HttpClient
from info_extractor import BilibiliInfoExtractor

class ResourceDownloader:
    def __init__(self, output_dir="output", log: callable = None):
        """
        :param output_dir: 下载保存目录
        :param log: 日志回调函数 log(str)
        """
        self.output_dir = output_dir
        self.log = log or (lambda s: print(s, flush=True))
        os.makedirs(self.output_dir, exist_ok=True)

    def download_all(self, video_info: dict):
        # 下载五件套（封面、弹幕、视频、音频、metadata）
        bvid = video_info["bvid"]
        save_dir = os.path.join(self.output_dir, bvid)
        os.makedirs(save_dir, exist_ok=True)

        # metadata
        self._save_metadata_json(video_info, save_dir)

        # 封面
        if video_info.get("cover_url"):
            self._download_cover(video_info["cover_url"], save_dir)

        # 弹幕
        if video_info.get("danmaku_url"):
            self._download_danmaku(video_info["danmaku_url"], save_dir, bvid)

        # 视频 + 音频 线程下载
        thread = threading.Thread(target=self.download_video_and_audio, args=(bvid, save_dir))
        thread.start()
        thread.join()

    def _save_metadata_json(self, video_info, save_dir):
        path = os.path.join(save_dir, "metadata.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(video_info, f, ensure_ascii=False, indent=4)
        self.log(f"[Metadata] metadata.json 已保存: {path}")

    def _download_cover(self, url, save_dir):
        cover_path = os.path.join(save_dir, "cover.jpg")
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        with open(cover_path, "wb") as f:
            f.write(resp.content)
        self.log(f"[Cover] 封面已保存: {cover_path}")

    def _download_danmaku(self, danmaku_url, save_dir, bvid):
        output_path = os.path.join(save_dir, "danmaku.xml")
        resp = HttpClient.get(
            danmaku_url,
            referer=f"https://www.bilibili.com/video/{bvid}/",
            timeout=15
        )
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        self.log(f"[Danmaku] 弹幕已保存: {output_path}")

    def download_video_and_audio(self, bvid: str, save_dir: str):
        os.makedirs(save_dir, exist_ok=True)
        video_path = os.path.join(save_dir, "video.mp4")
        mp3_path = os.path.join(save_dir, "video.mp3")
        url = f"https://www.bilibili.com/video/{bvid}"

        try:
            ydl_opts = {
                "outtmpl": os.path.join(save_dir, "video.%(ext)s"),
                "format": "bv+ba/b",
                "merge_output_format": "mp4",
                "noplaylist": True,
                "quiet": False,  # 可以看下载进度
            }
            print(f"[DEBUG] 开始下载 {bvid} 到 {save_dir}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"[Video] 视频已保存: {video_path}")

            if os.path.exists(video_path):
                cmd = [
                    "ffmpeg", "-y", "-i", video_path,
                    "-vn", "-acodec", "libmp3lame", "-q:a", "2", mp3_path
                ]
                try:
                    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                    print(f"[Audio] 音频已提取: {mp3_path}")
                except subprocess.CalledProcessError as e:
                    print(f"[Audio ERROR] 提取失败: {e.stderr.decode('utf-8')}")
            else:
                print(f"[Audio] 视频文件不存在，跳过音频提取: {video_path}")

        except Exception as e:
            print(f"[Video/Audio ERROR] {bvid} 下载失败: {e}")
        finally:
            gc.collect()
