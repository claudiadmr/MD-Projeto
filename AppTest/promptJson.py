import amazon_reviews
import openai
import json
import os

openai.api_key = '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' 

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def main(amazon, amazon_value):
    json_file = amazon
    with open(json_file, "r") as file:
        data = json.load(file)
    reviews = []
    for review_list in data:
        for review in review_list:
            reviews.append(review['body'])
    prompt = f"""
    Analyze the following collection of reviews and employ topic modeling techniques to categorize the feedback into specific features of the product.
    Divide each feature in positive characteristics and in negative characteristics, written it by your own words.
    Response format: 
                    
                    "features":       
                        -Name: x
                        -Product name: q
                        -Positive characteristics: y
                        -Negative characteristics: z 
                        -If there are no positive or negative characteristics, write "Not applicable".

    Provide it in JSON format to save in JSON file.

    Review text: '''{reviews}'''
    """
    response = get_completion(prompt)
    with open('response.json', 'w', encoding='utf-8') as f:
        f.write(response)
    return response