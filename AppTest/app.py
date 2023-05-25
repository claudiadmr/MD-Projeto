from flask import Flask, request, render_template, redirect
from dominate import document
from dominate.tags import *
import json
import amazon_reviews
import promptJson
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze_reviews', methods=['GET', 'POST'])
def analyze_reviews():
    if request.method == 'GET':
        return redirect('/')
    product_id = request.form.get('product_id')
    if not product_id:
        return 'Error: No product_id provided. Please go back and enter a product_id.', 400

    amazon, amazon_value = amazon_reviews.search(product_id)
    response = promptJson.main(amazon, amazon_value)
    data = json.loads(response)

    doc = document(title='Product Analyzer - ' + data['features'][0]['Product name'])

    with doc.head:
        link(rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/5.0.0/css/bootstrap.min.css')
        link(href='https://fonts.googleapis.com/css2?family=Lato:wght@300;400;500;700&display=swap', rel='stylesheet')
        style("""
                body {
                    font-family: 'Lato', sans-serif;
                    background-color: #ebf8fd;  /* Change background color */
                    display: flex;
                    flex-direction: column;
                    min-height: 100vh;
                    padding-bottom: 30px;  /* Add padding equal to footer height */
                    box-sizing: border-box;
                }
                .navbar {
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
                }
                .container {
                    max-width: 700px;
                    margin: 0 auto;
                    flex: 1;
                }
                .card {
                    border-radius: 15px;
                    box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15);
                    transition: transform .2s;
                    padding: 10px;  /* Add padding around card content */
                    margin-bottom: 20px;  /* Add more space between cards */
                    background-color: #ffffff;  /* Set card background color to white */
                }
                .card:hover {
                    transform: scale(1.03);
                }
                .positive {
                    color: #00796b;
                }
                .negative {
                    color: #b71c1c;
                }
                .footer {
                    position: fixed;
                    bottom: 0;
                    width: 100%;
                    height: 30px;  /* Increase the height */
                    line-height: 1px;  /* Corresponding increase in line height */
                    background-color: #f8f9fa;
                    text-align: center;
                    border-top: 1px solid #dee2e6;
                    color: #6c757d;
                    font-weight: bold;
                    font-size: 16px;
                }
            """)

    with doc:
        with div(cls='container my-4'):
            h1(f'{data["features"][0]["Product name"]} - Product ID: {amazon_value}', 
            cls='text-center text-primary mb-3')
            for feature in data['features']:
                with div(cls='card mb-3'):
                    with div(cls='card-body text-center'):
                        h2(feature['Name'], cls='card-title')
                        with div(cls='row'):
                            with div(cls='col positive text-center'):
                                h3('Positive characteristics:')
                                p(feature['Positive characteristics'])
                            with div(cls='col negative text-center'):
                                h3('Negative characteristics:')
                                p(feature['Negative characteristics'])
        with div(cls='footer'):
            p('UMinho - ' + date.today().strftime('%Y'))

    return str(doc), 200

if __name__ == "__main__":
    app.run(port=5000)
