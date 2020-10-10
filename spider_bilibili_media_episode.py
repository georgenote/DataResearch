# Bilibili_spider  - media_episode

## import library

import requests
from bs4 import BeautifulSoup

import pandas as pd
import json


class SpiderBilibiliMediaEpisode(object):

    def  __init__(self, media_id='md28229420'):
        '''
        :param media_id: the media's, eg: mdxxxxx.
        '''
        self.media_url = 'https://www.bilibili.com/bangumi/media/' + media_id

        self.headers = {
            'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }

        self.str_start = 32

        self.episode_base_url = 'https://api.bilibili.com/pgc/web/season/section?season_id='

    def get_season_id(self):

        season_id = None

        r = requests.get(url=self.media_url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        ## 判断season_id所在的json
        for content in soup.body.find_all(name='script'):
            content = str(content)

            if content[:self.str_start] == '<script>window.__INITIAL_STATE__':
                str_end = content.find('function') - 2
                data = content[self.str_start+1:str_end]
                data = json.loads(data)
                season_id = data['mediaInfo']['season_id']

        return season_id

    def get_episode_info(self, season_id):

        episode_url = self.episode_base_url + str(season_id)

        r = requests.get(url=episode_url, headers=self.headers)

        df = r.json()['result']['main_section']['episodes']

        episode_data = {}

        for data in df:

            episode_title = data['title']
            episode_longtitle = data['long_title']
            episode_id = data['id']

            episode_content = {
                'title': episode_title,
                'longtitle': episode_longtitle
            }

            episode_data[episode_id] = episode_content

        print(episode_data)

    def main(self):

        season_id = self.get_season_id()
        self.get_episode_info(season_id)


if __name__ == "__main__":
    spider = SpiderBilibiliMediaEpisode()
    spider.main()
