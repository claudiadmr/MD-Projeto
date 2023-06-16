from flask import Flask, request, render_template, redirect
import webscraping

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyze_reviews', methods=['GET'])
def analyze_reviews():
    if request.method == 'GET':
        amazon = request.args.get("product_id_amazon")
        walmart = request.args.get("product_id_walmart")
        datat = webscraping.run_scraper(amazon, walmart)

        return render_template('reviews.html', data=datat)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
