import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

res_list = []


def currents(func,args,nums):

    executor = ThreadPoolExecutor(max_workers=nums)

    future_tasks = [executor.submit(func, arg) for arg in args]

    wait(future_tasks, return_when=ALL_COMPLETED)

    for res in future_tasks:
        print(res.done())
        print(res.result())
        res_list.extend(res.result())
    return res_list