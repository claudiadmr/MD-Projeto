from requests_html import HTMLSession
import random
import json
import time
from proxylist import ProxyList

class Reviews:
    def __init__(self, asin, api_key):
        self.asin = asin
        self.api_key = api_key
        self.base_url = "http://api.scraperapi.com/?api_key={}&url=".format(api_key)
        self.url = f'https://www.amazon.co.uk/product-reviews/{self.asin}/ref_cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='
        self.session = HTMLSession()

    def pagination(self, page):
        headers = {'User-Agent': random.choice(user_agent_list)}
        proxy_list = Proxylist(country=['GB'])  # Filter proxies by country if desired
        proxy = random.choice(proxy_list.proxies)
        url = self.base_url + self.url + str(page) + '&proxy=' + proxy
        response = self.session.get(url, headers=headers)
        if response.status_code == 200 and 'div[data-hook=review]' in response.html.raw_html.decode():
            return response.html
        else:
            return False

    def parse(self, html):
        total = []
        reviews = html.find('div[data-hook=review]')
        for review in reviews:
            title = review.find('a[data-hook=review-title]', first=True).text
            rating = review.find('i[data-hook=review-star-rating] span', first=True).text
            body = review.find('span[data-hook=review-body] span', first=True).text.replace('\n', '').strip()

            data = {
                'title': title,
                'rating': rating,
                'body': body
            }
            total.append(data)
        return total

    def save_json(self, results):
        with open(self.asin + '-reviews_2.json', 'w') as f:
            json.dump(results, f)


if __name__ == '__main__':
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    amz = Reviews('B0779B2K8B', 'YOUR_SCRAPER_API_KEY')
    results = []
    for x in range(1, 5):
        print('getting page', x)
        time.sleep(0.3)
        html = amz.pagination(x)
        if html is not False:
            results.append(amz.parse(html))
        else:
            print('no more pages')
            break

    amz.save_json(results)
