import json
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.schema import Document
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = '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'

# Set the file path
file_path = 'B09MW19JW2_reviews.json'

# Load the JSON file
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract the data you need
documents = []
for item in data:
    document = Document(
        page_content=item['text'],
        metadata={
            'title': item['title'],
            'rating': item['rating']
        }
    )
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
response = qa_interface("""Analyze the following collection of reviews and employ topic modeling techniques to categorize the feedback into specific features of the product. Divide each feature in positive characteristics and in negative characteristics. Write the positive and negative features in a brief and objective manner as if you were writing for a technology website.

    Response format: 
                    
                    "features":       
                        -Name: x
                        -Positive characteristics: y
                        -Negative characteristics: z 
                        -If there are no positive or negative characteristics, write "Not applicable".

    Provide it in JSON format to save in JSON file.""")
print(response)
print(response['result'])
