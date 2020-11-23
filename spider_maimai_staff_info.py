#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import json
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

import warnings

warnings.filterwarnings("ignore")

class GetStaffInfo(object):
    """
    爬取脉脉目标公司的人员基础信息，写入csv文件。
    1. 基于搜索词搜索相关列表页 / 基于cookies登陆
    2. 遍历访问页面，获取人员信息
    3. 写入json文件
    """
    def __init__(self, cookie):
        self.cookie = cookie
        self.headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'cookie': self.cookie
        }

        # search_base_data
        self.search_base_url = 'https://maimai.cn/search/contacts'

        self.search_count = '20'
        self.search_dist = '0'
        self.search_tokens = ''
        self.search_highlight = 'true'
        self.search_jsononly = '1'
        self.search_pc = '1'

        self.staff_home_url = 'https://maimai.cn/contact/detail/'

        self.staff_fr = ''
        self.staff_from = 'pc_web_search'
        self.staff_position = ''
        self.staff_recid = ''
        self.staff_outofrel = 'false'
        self.staff_page_type = ''
        self.staff_sid = ''
        self.staff_job_popup = ''
        self.staff_job_dialog = ''
        self.staff_is_node = '1'

        self.script_end_num = 31

    def get_staff_list(self, search_page, search_word, data_base_info):
        """
        获取目标公司相关人员主页信息
        :data_base_info: {uid:encode_mmid}
        """

        params_search_query = {
            'count': self.search_count,
            'page': search_page,
            'query': search_word,
            'dist': self.search_dist,
            'searchTokens': self.search_tokens,
            'highlight': self.search_highlight,
            'jsononly': self.search_jsononly,
            'pc': self.search_pc
        }

        try:
            r = requests.get(url=self.search_base_url, headers=self.headers, params=json.dumps(urlencode(params_search_query)), verify=False)

            if r.status_code == 200:
                data = r.json()
                data = data['data']['contacts']

                num = len(data)

                for n in range(num):
                    uid = str(data[n]['uid'])
                    #name = data[n]['contact']['name']
                    encode_mmid = data[n]['contact']['encode_mmid']
                    data_base_info[uid] = encode_mmid

                return data_base_info

            else:
                print('status_code:{status_code}'.format(status_code=r.status_code))

        except Exception as e:
            print(e)

    def get_staff_info(self, data_base_info):
        """
        获取目标对象职业相关信息
        :data_staff_info:{'name':name, 'gender':gender, 'career':career, 'school':school}
        """

        params_staff_info = {
            'fr': self.staff_fr,
            'from': self.staff_from,
            'position': self.staff_position,
            'recid': self.staff_recid,
            'outofrel': self.staff_outofrel,
            'page_type': self.staff_page_type,
            'sid': self.staff_sid,
            'job_popup': self.staff_job_popup,
            'job_dialog': self.staff_job_dialog,
            'is_node': self.staff_is_node
        }

        data_staff_infotable = {}

        # cnt = 0
        num = len(data_base_info)


        for encode_mmid in data_base_info.values():

            # cnt += 1

            # if cnt in (12, 18, 30, 31, 32):
            staff_home_url = self.staff_home_url + encode_mmid

            try:
                r = requests.get(url=staff_home_url, headers=self.headers, params=json.dumps(urlencode(params_staff_info)), verify=False)

                if r.status_code == 200:

                    url = r.url

                    data_staff_info = {}
                    data_education = {}
                    data_career = {}

                    soup = BeautifulSoup(r.content, 'lxml')

                    content = str(soup.body.find(name='script'))
                    content = str(content.replace('\\', '%').encode('unicode-escape')).replace('%', '\\\\').replace('\\\\', '\\').encode().decode('unicode-escape').replace('"fr"', 'fr"').replace('\\', '').replace('"is_node":"1""','"is_node":"1"')

                    data = str(content).split(";")

                    num_split = len(data)

                    if num_split >= 11:

                        data_temp = ''
                        aim_split = int(num_split-2+1)

                        for t in range(8, aim_split):
                            data_temp = data_temp + data[t]

                        data = data_temp
                    else:
                        data = data[-2]

                    try:
                        data = data[data.find('"')+1:data.rfind('"')]
                        data = json.loads(data)

                    except Exception as e:
                        print(e)
                        print(num_split, data)

                    # 基础信息
                    card = data['data']['card']
                    mmid = card['mmid'] # mmid
                    name = card['name'] # 姓名
                    gender = card['gender'] # 性别 1:男; 2:女

                    uid = '{name}:{mmid}'.format(name=name, mmid=mmid)

                    uinfo = data['data']['uinfo']

                    # 教育
                    education = uinfo['education']
                    num_education = len(education)

                    for e in range(num_education):
                        school = education[e]['school']
                        department = education[e]['department']
                        degree = education[e]['degree']  # 1:本科 9:高中

                        if 'start_date' in education[e].keys():
                            school_start_date = education[e]['start_date']
                        else:
                            school_start_date = None

                        if 'end_date' in education[e].keys():
                            school_end_date = education[e]['end_date']
                        else:
                            school_end_date = None


                        data_school = {
                            'degree': degree,
                            'department': department,
                            'start_date': school_start_date,
                            'end_date': school_end_date
                        }

                        data_education[school] = data_school

                    school = None
                    department = None
                    school_start_date = None
                    school_end_date = None
                    degree = None

                    # 工作
                    career = uinfo['work_exp']
                    num_career = len(career)

                    for c in range(num_career):
                        company = career[c]['company']
                        department = career[c]['department']
                        career_start_date = career[c]['start_date']
                        career_end_date = career[c]['end_date']
                        position = career[c]['position']
                        description = career[c]['description']

                        data_company = {
                            'department': department,
                            'start_date': career_start_date,
                            'end_date': career_end_date,
                            'position': position,
                            'description': description
                        }

                        data_career[company] = data_company

                    company = None
                    department = None
                    career_start_date = None
                    career_end_date = None
                    position = None
                    description = None

                    # 个人信息
                    data_staff_info = {
                        'url': url,
                        'gender': gender,
                        'career': data_career,
                        'school': data_education
                    }

                    data_staff_infotable[uid] = data_staff_info
                    # print(cnt, name, data_staff_info)

                    uid = None
                    mmid = None
                    name = None
                    gender = None

                    time.sleep(1)

                else:
                    print('r.status_code:{status_code}'.format(status_code=r.status_code))

            except Exception as e:
                print(e)

        return data_staff_infotable, num

    def insert_staff_info(self, data_staff_info, filename, data_sum):
        """
        将获取到的数据写入本地备用
        """

        num = len(data_staff_info)

        print(data_staff_info)

        with open('./{company}_员工数据.json'.format(company=filename), 'w') as f:
            f.write(json.dumps(data_staff_info, ensure_ascii=False))

            print('{company}数据写入完成, 扫描{sum}条，写入{num}条数据.'.format(company=filename, sum=data_sum, num=num))


if __name__ == "__main__":

    # 需要修改的设置
    cookie = ''
    search_page_num = 5 # num * 20
    search_word_text = ['xx','yy']

    # 基础设置
    data_num = 0
    data_info_list = {}

    get_staff_info = GetStaffInfo(cookie)

    # 获取目标公司基础列表
    for word in search_word_text:

        print(word)

        for num in range(search_page_num):
            time.sleep(1)
            data_info_list = get_staff_info.get_staff_list(num, word, data_info_list)

        # 遍历访问，获取对象基础信息
        data_info, num = get_staff_info.get_staff_info(data_info_list)

    # 写入保存数据
    get_staff_info.insert_staff_info(data_info, search_word_text[0], num)
