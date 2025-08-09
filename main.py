import os
from info_extractor import BilibiliInfoExtractor
from resource_downloader import ResourceDownloader
from info_data import append_video_info, init_excel

def load_bvid_list(file_path: str):
    if not os.path.exists(file_path):
        print(f"[Error] 找不到 {file_path}，请创建并写入BV号")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    extractor = BilibiliInfoExtractor()
    downloader = ResourceDownloader(output_dir="output")

    if not os.path.exists("output.xlsx"):
        init_excel("output.xlsx")

    bvid_list = load_bvid_list("bvid_list.txt")
    if not bvid_list:
        print("[Info] 没有需要处理的 BV 号")
        return

    print(f"[Main] 共 {len(bvid_list)} 个视频等待处理")

    for idx, bvid in enumerate(bvid_list, start=1):
        print(f"\n[Main] ({idx}/{len(bvid_list)}) 正在处理 {bvid} ...")
        try:
            video_info = extractor.get_video_info(bvid)
            video_info["url"] = f"https://www.bilibili.com/video/{bvid}"
            print(f"[Debug] video_info keys: {list(video_info.keys())}")

            downloader.download_all(video_info)
            append_video_info("output.xlsx", video_info)

        except Exception as e:
            print(f"[Error] 处理 {bvid} 时出错: {e}")

    print("\n[Main] 所有任务完成")

if __name__ == "__main__":
    main()
