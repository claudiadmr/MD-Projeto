import requests
import threading
from flask import jsonify
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.schema import Document
import os
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class APIRequestThread(threading.Thread):
    def __init__(self, url):
        self.data = None
        self.url = url
        threading.Thread.__init__(self)

    def run(self):
        response = requests.get(self.url)
        self.data = response.json()


def run_scraper(amazon, walmart):
    url1 = f'http://127.0.0.1:9080/crawl.json?spider_name=amazon_reviews&start_requests=true&crawl_args={{"asin": "{amazon}"}}'
    url2 = f'http://127.0.0.1:9080/crawl.json?spider_name=wallmart_reviews&start_requests=true&crawl_args={{"asin": "{walmart}"}}'

    thread1 = APIRequestThread(url1)
    thread2 = APIRequestThread(url2)

    # Start both threads
    thread1.start()
    thread2.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()

    # Combine data from both threads
    combined_data = {
        'data1': thread1.data,
        'data2': thread2.data,
    }
    print(len(combined_data['data1']['items']))
    print(len(combined_data['data2']['items']))
    combined_data = combined_data['data1']['items'] + combined_data['data2']['items']
    print(len(combined_data))
    return jsonify(combined_data)


def joinScrapyData():
    import json
    with open("static/response.json") as json_file:
        data = json.load(json_file)
        # data['data1'] = data['data1']['items']
        # data['data2'] = data['data2']['items']
        # data = data['data1'] + data['data2']
        print(len(data))
    return data


def openaiRequest():
    data = joinScrapyData()
    documents = []
    for item in data:
        metadata = {'rating': item['rating']}
        if item['title'] is not None:
            metadata['title'] = item['title']
        if item['product'] is not None:
            metadata['product'] = item['product']

        document = Document(page_content=item['text'], metadata=metadata)
        documents.append(document)

    # Split the text in chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Create a persistent, file-based vector store
    directory = 'index_store'
    vector_index = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=directory)
    vector_index.persist()

    # Create the retriever and the query-interface
    retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    qa_interface = RetrievalQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", retriever=retriever,
                                               return_source_documents=True)

    # Query GPT-3
    response = qa_interface("""Please analyze the following collection of reviews and extract the relevant features for the product. 
    For each feature, provide a list of positive and negative comments. Response format: 
    featureName: 
    -name: x 
    -Positive Feature Reviews: (only the ones about this feature) 
    -Negative Feature Reviews: (only the ones about this feature) 
    If there are no positive or negative characteristics, write “Not applicable”. 
    Provide it in JSON format.""")
    print(response)
    print(response['result'])
    return response['result']
