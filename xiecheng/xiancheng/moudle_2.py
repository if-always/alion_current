import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


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
    for picture_name, picture_link in zip(picture_name_list, picture_link_list):
        urllib.request.urlretrieve(picture_link, '/home/lin/img/douban_books/%s.jpg' % picture_name)
    return picture_name_list

def main():

    res_list = []
    start_urls = ["https://movie.douban.com/top250"]
    for i in range(1, 10):
        start_urls.append("https://movie.douban.com/top250?start=%d&filter=" % (25 * i))

    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 利用并发下载电影图片
    executor = ThreadPoolExecutor(max_workers=10)  # 可以自己调整max_workers,即线程的个数
    # submit()的参数： 第一个为函数， 之后为该函数的传入参数，允许有多个
    future_tasks = [executor.submit(download_picture, url) for url in start_urls]
    # 等待所有的线程完成，才进入后续的执行
    #print(future_tasks)
    wait(future_tasks, return_when=ALL_COMPLETED)

    t4 = time.time()
    for res in future_tasks:
        print(res.done())
        print(res.result())
        res_list.extend(res.result())
    print(res_list)
    print('使用多线程，总共耗时：%s' % (t4 - t3))
    print('*' * 50)

if __name__ == '__main__':
    main()
