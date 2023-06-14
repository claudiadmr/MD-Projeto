import requests
import threading

from flask import jsonify


class APIRequestThread(threading.Thread):
    def __init__(self, url):
        self.data = None
        self.url = url
        threading.Thread.__init__(self)

    def run(self):
        response = requests.get(self.url)
        self.data = response.json()


def run_scraper(amazon, walmart):
    url1 = f'http://127.0.0.1:9080/crawl.json?spider_name=amazon_reviews&start_requests=true&crawl_args={{"asin": "{amazon}"}}'
    url2 = f'http://127.0.0.1:9080/crawl.json?spider_name=wallmart_reviews&start_requests=true&crawl_args={{"asin": "{walmart}"}}'

    thread1 = APIRequestThread(url1)
    thread2 = APIRequestThread(url2)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Combine data from both threads
    combined_data = {
        'data1': thread1.data,
        'data2': thread2.data,
    }

    return jsonify(combined_data)
