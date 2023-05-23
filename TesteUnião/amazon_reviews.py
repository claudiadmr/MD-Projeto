from requests_html import HTMLSession
import json
import time
import random
import pandas as pd

class ReviewScraper:
    def __init__(self, asin):
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]

        user_agent = random.choice(user_agent_list)
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent': user_agent}
        self.url = f'https://www.amazon.co.uk/product-reviews/{self.asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='


    def pagination(self, page):
        r = self.session.get(self.url + str(page), headers=self.headers)
        
        if r.status_code == 200:
            if not r.html.find('div[data-hook=review]'):
                return False
            else:
                return r.html.find('div[data-hook=review]')
        else:
            print("Request failed with status code:", r.status_code)
            return False

    def parse(self, reviews):
        total = []
        for review in reviews:
            title_elem = review.find('a[data-hook=review-title]',first=True)
            title = title_elem.text if title_elem is not None else "N/A"

            rating_elem = review.find('i[data-hook=review-star-rating] span',first=True)
            rating = rating_elem.text if rating_elem is not None else "N/A"

            body_elem = review.find('span[data-hook=review-body] span',first=True)
            body = body_elem.text.replace('\n','').strip() if body_elem is not None else "N/A"

            data={
                'title': title,
                'rating': rating,
                'body': body
            }
            total.append(data)
        return total


    def save_json(self, results):
        #print(self.asin)
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f, indent=4)


def search(): 
    results = []
    for x in range(1,2):
        value = input("Indique o ID do produto que deseja: ")
        amz = ReviewScraper(value)
        #print('getting page',x)
        time.sleep(10)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.append(amz.parse(reviews))
        else:
            print('no more pages')
            break

    amz.save_json(results)
    value_json = value  + '-reviews.json'

    return value_json, value


if __name__ == '__main__':
    search()