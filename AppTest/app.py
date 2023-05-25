from flask import Flask, request, render_template
from dominate import document
from dominate.tags import *
import json
import amazon_reviews
import promptJson

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze_reviews', methods=['POST'])
def analyze_reviews():
    product_id = request.form.get('product_id')
    if not product_id:
        return 'Error: No product_id provided. Please go back and enter a product_id.', 400

    amazon, amazon_value = amazon_reviews.search(product_id)
    response = promptJson.main(amazon, amazon_value)
    data = json.loads(response)

    doc = document(title='Product Analyzer - ' + data['features'][0]['Product name'])

    with doc.head:
        link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css')
        link(href='https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap', rel='stylesheet')
        style("""
            body {
                font-family: 'Roboto', sans-serif;
            }
            .card {
                border-radius: 15px;
                box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15)!important;
            }
            .positive {
                color: #00876c;
            }
            .negative {
                color: #d43f3a;
            }
        """)

    with doc:
        with div(cls='container my-5'):
            h1(f'{data["features"][0]["Product name"]} - Product ID: {amazon_value}', 
            cls='text-center text-primary mb-4')
            for feature in data['features']:
                with div(cls='card my-3'):
                    with div(cls='card-body'):
                        h2(feature['Name'], cls='card-title')
                        with div(cls='positive'):
                            h3('Positive characteristics:')
                            p(feature['Positive characteristics'])
                        with div(cls='negative'):
                            h3('Negative characteristics:')
                            p(feature['Negative characteristics'])

    return str(doc), 200


if __name__ == "__main__":
    app.run(port=5000)
