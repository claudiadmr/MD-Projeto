from flask import Flask, request, render_template, redirect

import webscraping

app = Flask(__name__)

@app.route('/analyze_reviews', methods=['GET'])
def analyze_reviews():
    if request.method == 'GET':
        amazon = request.args.get('amazon')
        walmart = request.args.get('walmart')
        return webscraping.run_scraper(amazon, walmart)


if __name__ == '__main__':
    app.run()
