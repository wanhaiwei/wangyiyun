import requests
from lxml import etree
import re
import csv
import json


class SingerSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36'
        }

    def get_index(self, url):
        '请求模块'
        try:
            resp = requests.get(url,headers=self.headers)
            if resp.status_code == 200:
                self.parse_re(resp.text)
            else:
                print('error')
        except ConnectionError:
            self.get_index(url)

    def parse_re(self, resp):
        '解析模块'
        print('start parse {}'.format(url))
        tags = re.findall(r'<a href=".*?/artist\?id=(\d+)" class="nm nm-icn f-thide s-fc0" title=".*?的音乐">(.*?)</a>', resp, re.S)
        title = re.findall(r'<title>(.*?)-.*?</title>', resp, re.S)
        for tag in tags:
            # print(tag[0],tag[1])
            # self.save_json(tag, title)
            self.save_csv(tag, title)

    def save_csv(self, tag, title):
        '存储模块'
        print('start save {}'.format(url))
        with open('all_singer.csv', 'a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((tag[0], tag[1], title[0]))
        print('finish spider {}'.format(url))

    def save_json(self, tag, title):
        print('start save {}'.format(url))
        s = json.dumps({'id': tag[0], 'name': tag[1], 'title': title[0]},ensure_ascii=False)
        with open('all_singer.json', 'a+', newline='', encoding='utf-8') as f:
            f.write(s)
        print('finish spider {}'.format(url))
        print(s)


if __name__ == '__main__':
    # 歌手分类id
    list1 = [1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003]
    # initial的值
    list2 = [0,65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
    for i in list1:
        for j in list2:
            url = 'http://music.163.com/discover/artist/cat?id=' + str(i) + '&initial=' + str(j)
            print('start spider {}'.format(url))
            SingerSpider().get_index(url)

