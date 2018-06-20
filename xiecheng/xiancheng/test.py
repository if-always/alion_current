import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from current import *

def download_picture(url):

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "lxml")

    content = soup.find('div', class_='article')
    images = content.find_all('img')
    # 获取电影图片的名称和下载地址
    picture_name_list = [image['alt'] for image in images]
    picture_link_list = [image['src'] for image in images]
    #print(picture_name_list)
    #return picture_name_list
    #利用urllib.request..urlretrieve正式下载图片
    #for picture_name, picture_link in zip(picture_name_list, picture_link_list):
    #    urllib.request.urlretrieve(picture_link, '/home/lin/img/douban_books/%s.jpg' % picture_name)
    return picture_name_list



res_list = []
start_urls = ["https://movie.douban.com/top250"]
for i in range(1, 10):
    start_urls.append("https://movie.douban.com/top250?start=%d&filter=" % (25 * i))


res = currents(download_picture,start_urls,10)
print(res)