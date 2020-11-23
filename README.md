# KnowTheWorld

## 一、Bilibili

### 1. spider_bilibili_episode_episode

**Input:** 视频id eg: media_id='md28229420' # 风犬少年的天空

**Output:** 特定视频各剧集的基础信息, json格式, eg: { epid: { id: id, title: title } }
> 剧集源Json中还有其他很多信息, 由于暂不需要, 因此未抽取, 可修改py文件进行增补

## 二、MaiMai

### 1. spider_maimai_staff_info.py

**Input:**
  * 账户cookie: 在爬取过程中一定要是脉脉会员, 否则无法访问3度人脉以外的主页.
  * 搜索页面想要请求的页数(一页20条)
  * 想要搜索的关键字(List 支持多条查询)

**Output:** 目标公司的职员信息, json格式, 包括教育与职业经历.

**待修复**
 [ ] 1. 某些情况下会出现单条爬取失败并且跳过该用户的情况, 已经定位到是由于"程序中某段基于文本按';'分隔的, 因此会因为具体文本出现分隔错误的情况", 不影响整体爬虫任务.
