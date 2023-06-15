import json
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.schema import Document
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = ''

# Set the file path
file_path = 'response.json'

# Load the JSON file
with open(file_path, 'r') as f:
    data = json.load(f)
    data['data1'] = data['data1']['items']
    data['data2'] = data['data2']['items']
    data = data['data1'] + data['data2']
    print(len(data))
# Extract the data you need
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
response = qa_interface("""Analyze the following collection of reviews and employ topic modeling techniques to categorize the feedback into specific features of the product.
Start by translating every review that is in another language to english.
Divide each feature in positive characteristics and in negative characteristics.
Response format: Feature:
                -name: x
                 -Positive Feature Reviews:( only the ones about this feature)
                 -Negative Feature Reviews:(only the ones about this feature)
If there are no positive or negative characteristics, write "Not applicable".
Provide it in JSON format.""")
print(response)
print(response['result'])
