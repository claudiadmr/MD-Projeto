import scrapy
from urllib.parse import urljoin

class WalmartReviewsSpider(scrapy.Spider):
    name = "wallmart_reviews"

    def __init__(self, asin=None, *args, **kwargs):
        super(WalmartReviewsSpider, self).__init__(*args, **kwargs)
        self.asin = asin
        self.product_name = None  # Add this line
        self.product_name_extracted = False # Flag to track if product name has been extracted
    def start_requests(self):
        wallmart_reviews_url = f'https://www.walmart.com/reviews/product/{self.asin}/'
        yield scrapy.Request(url=wallmart_reviews_url, callback=self.parse_reviews, meta={'asin': self.asin, 'retry_count': 0})


    def parse_reviews(self, response):
        asin = response.meta['asin']
        retry_count = response.meta['retry_count']

        ## Get Next Page Url
        next_page_relative_url = response.css('a[data-testid="NextPage"]::attr(href)').get()
        if next_page_relative_url is not None:
            retry_count = 0
            next_page = urljoin('https://www.walmart.com/', next_page_relative_url)
            yield scrapy.Request(url=next_page, callback=self.parse_reviews, meta={'asin': asin, 'retry_count': retry_count})
        
        ## Adding this retry_count here to bypass any amazon js rendered review pages
        elif retry_count < 3:
            retry_count = retry_count+1
            yield scrapy.Request(url=response.url, callback=self.parse_reviews, dont_filter=True, meta={'asin': asin, 'retry_count': retry_count})

      ## Extract Product Name
        if not self.product_name_extracted:
            self.product_name = response.css('a[class="w_x7ug f6 dark-gray"]::text').get().split(",")[0]
            words = self.product_name.split()
            self.product_name = ' '.join(words[2:])
        
      ## Parse Product Reviews
        review_elements = response.css("ul.cc-3.cg-4.pl0.mt4 li.dib.w-100.mb3")
        for review_element in review_elements:
            rating_element = review_element.css("span.w_iUH7::text").get()
            rating = rating_element.split()[0] if rating_element else None

            title_element = review_element.css("span.b.w_V_DM::text").get()
            title = title_element.strip() if title_element else None
            text_element = review_element.css("span.tl-m::text").get()
            text = text_element.strip() if text_element else None

            if text is not None:
                yield {
                    "asin": asin,
                    "product": self.product_name,
                    "text": text,
                    "title": title,
                    "rating": rating,
                    "source": "wallmart"
                }
            