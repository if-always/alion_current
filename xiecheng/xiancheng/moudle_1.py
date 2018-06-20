import requests, re, string
import threading, queue, time
import sys
from requests.exceptions import RequestException

_DATA = []
FILE_LOCK = threading.Lock()
SHARE_Q = queue.Queue()  #构造一个不限制大小的的队列
_WORKER_THREAD_NUM = 6  #设置线程的个数


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
           }

class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑

    def run(self) :
        self.func()

def worker() :
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get() #获得任务
        html = get_html(url)
        get_datas(html)
        time.sleep(1)
        SHARE_Q.task_done()

def get_html(url) :

    try:
        res = requests.get(url,headers = headers)
        if res.status_code == 200:
            return res
        else:
            return None
    except RequestException:
        return None

def get_datas(html) :

    temp_data = []
    movie_items = re.findall('<span.*?class="title">(.*?)</span>', html.text, re.S)
    #print(movie_items)
    for index, item in enumerate(movie_items) :
        if item.find("&nbsp") == -1 :
            print (item)
            temp_data.append(item)
    _DATA.append(temp_data)


def main() :
    global SHARE_Q
    threads = []
    douban_url = "http://movie.douban.com/top250?start={page}&filter=&type="

    for index in range(10) :
        SHARE_Q.put(douban_url.format(page = index * 25))
    for i in range(1) :
        thread = MyThread(worker)
        thread.start()  #线程开始处理任务
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()
    print(_DATA)
    print ("Spider Successful!!!")

if __name__ == '__main__':
    main()