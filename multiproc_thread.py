__author__ = 'crimzoid'


from queue import Queue
from threading import Thread
import requests

unvisited_urls = Queue()
D = []

def do_work(urls):
    D.append(requests.get(urls))


def visit_urls():
    while True:
        do_work(unvisited_urls.get())
        unvisited_urls.task_done()
        if unvisited_urls.empty:
            break




def construct_nw_urls():
    base_url = 'http://netwars.pl/temat/{0!s}'
    return (base_url.format(n) for n in range(170020, 170050))


def add_urls_to_q():
    for url in construct_nw_urls():
        unvisited_urls.put(url)


def run(number_of_worker_threads):
    add_urls_to_q()
    for _ in range(number_of_worker_threads):
        worker = Thread(target=visit_urls, daemon=False)
        worker.start()
        print('bla')

    unvisited_urls.join()



def bench_no_threads():
    D = []
    for url in construct_nw_urls():
        D.append(requests.get(url))
    return D


run(10)