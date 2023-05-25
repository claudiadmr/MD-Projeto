from requests_html import HTMLSession
import json
import time
import random

class Reviews:
    def __init__(self, asin) -> None:
        user_agent_list = [ 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
        ]
        user_agent = random.choice(user_agent_list)
        self.asin = asin
        self.session = HTMLSession()
        self.headers = {'User-Agent': user_agent}
        self.url = f'https://www.amazon.co.uk/product-reviews/dp/{self.asin}/ref_cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='

    def pagination(self, page):
        r = self.session.get(self.url + str(page))
        if not r.html.find('div[data-hook=review]'):
            return False
        else:
            return r.html.find('div[data-hook=review]')

    def parse(self, reviews):
        total = []
        for review in reviews:
            title = review.find('a[data-hook=review-title]',first=True).text
            rating = review.find('i[data-hook=review-star-rating] span',first=True).text
            body = review.find('span[data-hook=review-body] span',first=True).text.replace('\n','').strip()
            data={
                'title': title,
                'rating': rating,
                'body': body
            }
            total.append(data)
        return total

    def save_json(self, results):
        with open(self.asin + '-reviews.json', 'w') as f:
            json.dump(results, f, indent=4)

def search(product_id): 
    results = []
    value = product_id
    for x in range(1,3):
        amz = Reviews(value)
        time.sleep(10)
        reviews = amz.pagination(x)
        if reviews is not False:
            results.append(amz.parse(reviews))
        else:
            break
    amz.save_json(results)
    value_json = value  + '-reviews.json'
    return value_json, value