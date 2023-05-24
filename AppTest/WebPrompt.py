from flask import Flask, request, render_template_string
from dominate import document
from dominate.tags import *
import json
import amazon_reviews
import promptJson

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
            }
            .container {
                background: #fff;
                padding: 30px;
                border-radius: 6px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 400px;
                width: 100%;
            }
            h1 {
                font-size: 24px;
                margin-top: 0;
                margin-bottom: 30px;
                text-align: center;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-label {
                display: block;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 8px;
            }
            .form-input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            .form-button {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 4px;
                background-color: #4CAF50;
                color: #fff;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
            }
            .form-button:hover {
                background-color: #45a049;
            }
        </style>
        <div class="container">
            <h1>Amazon Product Analyzer</h1>
            <form method="POST" action="/analyze_reviews">
                <div class="form-group">
                    <label for="product_id" class="form-label">Product ID:</label>
                    <input type="text" id="product_id" name="product_id" class="form-input" placeholder="Enter the product ID...">
                </div>
                <button type="submit" class="form-button">Analyze</button>
            </form>
        </div>
    """)

@app.route('/analyze_reviews', methods=['POST'])
def analyze_reviews():
    product_id = request.form.get('product_id')
    if not product_id:
        return 'Error: No product_id provided. Please go back and enter a product_id.', 400
    amazon, amazon_value = amazon_reviews.search(product_id)
    response = promptJson.main(amazon, amazon_value)

    print(response)  # Add this line to check the value of the response

    # Generate HTML from response
    data = json.loads(response)
    doc = document(title='Features')

    with doc.head:
        style("""
            body {
                font-family: Arial, sans-serif;
            }
            .feature {
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-bottom: 20px;
                padding: 20px;
                background-color: #fff;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            .feature-name {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin: 0 0 10px;
            }
            .positive {
                color: #27ae60;
                font-weight: bold;
            }
            .negative {
                color: #c0392b;
                font-weight: bold;
            }
        """)

    with doc:
        product_name = data['Features'][0]['Product name']
        h1(f' {product_name} - Product ID: {amazon_value}', style="text-align:center; color: #333;")
        for feature in data['Features']:
            with div(cls='feature'):
                h2(feature['Name'], cls='feature-name')
                with div(cls='positive'):
                    h3('Positive characteristics:')
                    p(feature['Positive characteristics'])
                with div(cls='negative'):
                    h3('Negative characteristics:')
                    p(feature['Negative characteristics'])

    return str(doc), 200

if __name__ == "__main__":
    app.run(port=5000)