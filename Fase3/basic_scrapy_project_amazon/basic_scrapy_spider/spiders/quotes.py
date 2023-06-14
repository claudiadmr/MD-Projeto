import scrapy
from urllib.parse import urljoin

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"

    def __init__(self, asin=None, *args, **kwargs):
        super(AmazonReviewsSpider, self).__init__(*args, **kwargs)
        self.asin = asin
        self.product_name = None  # Add this line
        self.product_name_extracted = False # Flag to track if product name has been extracted

    def start_requests(self):
        amazon_reviews_url = f'https://www.amazon.com/product-reviews/{self.asin}/'
        yield scrapy.Request(url=amazon_reviews_url, callback=self.parse_reviews, meta={'asin': self.asin, 'retry_count': 0})

    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']


        ## Get Next Page Url
        next_page_relative_url = response.css(".a-pagination .a-last>a::attr(href)").get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.amazon.com/', next_page_relative_url)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': retry_count})

        ## Adding this retry_count here to bypass any Amazon JS-rendered review pages
        elif retry_count < 3:
            retry_count = retry_count + 1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=True,
                                 meta={'asin': asin, 'retry_count': retry_count})

        ## Extract Product Name (Only for the first time)
        if not self.product_name_extracted:
            self.product_name = response.css("*[data-hook*=product-link]::text").get().split(",")[0]
            self.product_name_extracted = True

        ## Parse Product Reviews
        review_elements = response.css("#cm_cr-review_list div.review")

        for review_element in review_elements:
            yield {
                "asin": asin,
                "product": self.product_name if self.product_name else None,
                "text": "".join(review_element.css("span[data-hook=review-body] ::text").getall()).strip(),
                "title": review_element.css("*[data-hook=review-title]>span::text").get(),
                "rating": review_element.css("*[data-hook*=review-star-rating] ::text").re(r"(\d+\.*\d*) out")[0],
                "source": "amazon"
            }
        
