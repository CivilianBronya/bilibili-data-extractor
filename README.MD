<p align="center">
  <h2 align="center">Bilibili data extractor</h2>
  <p align="center">
    一个基于网页和API结合的B站视频信息抓取工具，支持视频数据采集与Excel导出。
    <br/>
    <br/>
    <a href="#"><strong>» 项目文档（待完善） »</strong></a>
    <br/>
  </p>
</p>
<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-3.8+-blue?logo=python&style=for-the-badge" alt="Python Version">
  </a>
  <a href="https://github.com/CivilianBronya/bilibili-data-extractor">
    <img src="https://img.shields.io/badge/Bilibili data extractor-开发中-blue?style=for-the-badge" alt="Github">
  </a>
  <a href="https://qm.qq.com/q/e6kdQbTVja">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-514280270-blue?style=for-the-badge" alt="QQ Group">
  </a>
  <a href="https://github.com/CivilianBronya/bilibili-data-extractor/stargazers">
    <img src="https://img.shields.io/github/stars/CivilianBronya/bilibili-data-extractor?color=F8B195&logo=github&style=for-the-badge" alt="Github stars">
  </a>
  <a href="https://github.com/CivilianBronya/bilibili-data-extractor/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/CivilianBronya/bilibili-data-extractor?color=C06C84&style=for-the-badge" alt="License">
  </a>
</p>


---

## 🚀 功能特点

- 结合网页爬取与官方API，提取B站视频详细信息  
- 自动抓取播放数、弹幕、点赞、投币、收藏、转发、标签、作者等数据  
- 支持批量处理BV号列表
- 导出数据到Excel文件，自动去重并追加爬取时间  
- 支持视频封面和弹幕XML链接获取  
- 代码结构清晰，方便扩展和二次开发  

---

## 🛠 快速开始
### 获取项目
- 通过git拉取到自己的本地，通过python运行

```bash
https://github.com/CivilianBronya/bilibili-data-extractor.git
```

### 环境准备
- Python 3.8+
- 依赖库：`requests`, `beautifulsoup4`, `openpyxl`

```bash
pip install requests beautifulsoup4 openpyxl
```

## 🌟 社区交流

加入粉丝群，获取本人对项目进度与开发、问题答疑和技术交流！

* QQ 交流群:
  * 本人QQ[粉丝群](https://qm.qq.com/q/ufcprjrHl6)可加入聊天潜水


> **提问前请先查看**: 加入Q群前，请先查看[项目问题列表](https://github.com/CivilianBronya/bilibili-data-extractor/issues)，看是否能解决你的问题。
> 
> 如需提问，请准备好问题描述、**完整日志**和相关配置文件，以便更好地帮助到你！
> 进群请备注：GitHub


## 🦊 使用方法
运行主程序：

```bash
python main.py
```
- 自动创建BVID_list.txt(可以自行创建)
- 自动创建并保存output.xlsx保存视频信息数据
- 自动保存视频内容，包括视频封面，弹幕信息，视频各类数据json文件，MP3音频，MP4视频，保存在output文件夹，以BV号进行保存

## 🛠 贡献者名单   

欢迎提出新的点子、 Pull Request。  

<a>暂未有任何贡献者，说不定下次就有你呢，喵~o( =∩ω∩= )m</a>

## 💪 支持项目

如果对这个项目感兴趣，请给我们一颗 ⭐️  
我们会继续开发该项目，直到结束或者暂停维护~
