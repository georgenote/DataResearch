# KnowTheWorld

## 一、Bilibili

### 1. spider_bilibili_episode_episode

**Input:** 视频id eg: media_id='md28229420' # 风犬少年的天空

**Output:** 特定视频各剧集的基础信息, json格式, eg: { epid: { id: id, title: title } }
> 剧集源Json中还有其他很多信息, 由于暂不需要, 因此未抽取, 可修改py文件进行增补

## 二、MaiMai

### 1. spider_maimai_staff_info.py

**Input:**
  * 脉脉会员cookie
  * 搜索页面想要请求的页数(一页20条)
  * 想要搜索的关键字(List 支持多条查询)
