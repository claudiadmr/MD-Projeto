from flask import Flask, request, render_template, redirect
import webscraping

app = Flask(__name__)

# Sample data
data = {
    "Price": {
        "Name": "Price",
        "Positive Reviews": ["Great for the price", "Excellent value for the mone Excellent value for the money Excellent value for the money Excellent value for the money Excellent value for the money Excellent value for the moneyy", "Affordable and high quality"],
        "Negative Reviews": ["Cheaply made", "You get what you pay forYou get what you pay forYou get what you pay forYou get what you pay forYou get what you pay for", "You get what you pay for", "You get what you pay for", "You get what you pay for", "You get what you pay for", "You get what you pay for"]
    },
    "Durability": {
        "Name": "Durability",
        "Positive Reviews": ["Built to last", "Sturdy construction", "Handles wear and tear well"],
        "Negative Reviews": ["Broke easily", "Not very sturdy", "Poor quality materials"]
    },
    "Durabilitys": {
        "Name": "Durabilitys",
        "Positive Reviews": ["Built to last", "Sturdy construction", "Handles wear and tear well"],
        "Negative Reviews": ["Broke easily", "Not very sturdy", "Poor quality materials"]
    },
    "Durabilityss": {
        "Name": "Durabilityss",
        "Positive Reviews": ["Built to last", "Sturdy construction", "Handles wear and tear well"],
        "Negative Reviews": ["Broke easily", "Not very sturdy", "Poor quality materials"]
    },
    "Durabilitysss": {
        "Name": "Durabilitysss",
        "Positive Reviews": ["Built to last", "Sturdy construction", "Handles wear and tear well"],
        "Negative Reviews": ["Broke easily", "Not very sturdy", "Poor quality materials"]
    }
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyze_reviews', methods=['GET'])
def analyze_reviews():
    if request.method == 'GET':
        amazon = request.args.get("product_id_amazon")
        walmart = request.args.get("product_id_walmart")
       # datat = webscraping.openaiRequest()
        #print(datat)

        # return webscraping.openaiRequest()
        return render_template('reviews.html', data=data)
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
