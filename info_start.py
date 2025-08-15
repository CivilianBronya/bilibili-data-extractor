import os
import time
import threading
from typing import Callable, Optional, Union

from info_extractor import BilibiliInfoExtractor
from resource_downloader import ResourceDownloader
from info_data import append_video_info, init_excel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_excel_lock = threading.Lock()


def _abs(p: Optional[Union[str, Callable]], default_name: str) -> str:
    if callable(p):
        p = None
    if p:
        return p if os.path.isabs(p) else os.path.join(BASE_DIR, str(p))
    return os.path.join(BASE_DIR, default_name)


def load_bvid_list(file_path: str):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _download_data(bvid: str, excel_path: str, logger: Callable[[str], None]):
    extractor = BilibiliInfoExtractor()
    video_info = extractor.get_video_info(bvid)
    video_info["url"] = f"https://www.bilibili.com/video/{bvid}"

    with _excel_lock:
        append_video_info(excel_path, video_info)
        logger(f"[Excel] 信息已写入: {bvid}")

    logger(f"[INFO] 信息提取完成: {video_info.get('title', '')}")
    return video_info


def _download_resources(video_info: dict, output_dir: str):
    try:
        downloader = ResourceDownloader(output_dir=output_dir)
        downloader.download_all(video_info)
    except Exception as e:
        print(f"[ERROR] 下载资源失败: {video_info.get('url')} - {e}", flush=True)


def run_extraction(
        bvid_file: Optional[Union[str, Callable]] = None,
        excel_path: Optional[Union[str, Callable]] = None,
        output_dir: Optional[Union[str, Callable]] = None,
        log: Optional[Callable[[str], None]] = None
):
    logger = log or (lambda msg: print(msg, flush=True))

    bvid_file = _abs(bvid_file, "BVID_list.txt")
    excel_path = _abs(excel_path, "output.xlsx")
    output_dir = _abs(output_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(excel_path):
        init_excel(excel_path)

    bvid_list = load_bvid_list(bvid_file)
    if not bvid_list:
        logger("[INFO] 没有需要处理的 BV 号")
        return

    logger(f"[MAIN] 共 {len(bvid_list)} 个视频等待处理")

    # 逐条顺序处理
    for idx, bvid in enumerate(bvid_list, start=1):
        logger(f"[MAIN] ({idx}/{len(bvid_list)}) 提取视频信息 {bvid} ...")
        try:
            video_info = _download_data(bvid, excel_path, logger)
        except Exception as e:
            logger(f"[ERROR] 提取 {bvid} 出错: {e}")
            continue

        logger(f"[MAIN] ({idx}/{len(bvid_list)}) 下载视频资源 {bvid} ...")
        try:
            _download_resources(video_info, output_dir)
        except Exception as e:
            logger(f"[ERROR] 下载 {bvid} 出错: {e}")

        # 可选：限制请求频率
        time.sleep(0.6)

    logger("[MAIN] 所有任务已完成")


def simple_logger(msg):
    print(msg)

if __name__ == "__main__":
    bvid_file = os.path.join(os.path.dirname(__file__), "BVID_list.txt")

    excel_path = os.path.join(os.path.dirname(__file__), "output.xlsx")

    output_dir = os.path.join(os.path.dirname(__file__), "output")

    os.makedirs(output_dir, exist_ok=True)

    run_extraction(
        bvid_file=bvid_file,
        excel_path=excel_path,
        output_dir=output_dir,
        log=simple_logger
    )

    print("测试完成！")