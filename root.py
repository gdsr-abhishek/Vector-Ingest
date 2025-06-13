from flask import Flask
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
import fitz
import glob
from langchain.document_loaders import  PyPDFLoader
app = Flask(__name__)
load_dotenv()
@app.route('/',methods=['GET'])
def root():
    # qdrant_client = QdrantClient(
    # url=os.getenv("QDRANT_URI"), 
    # api_key=os.getenv("QDRANT_API_KEY"),
    # )
    # doc = fitz.open("./docs/aws-sdk-ref.pdf")
    # print(f'number of pages: {doc.page_count}')
    # return qdrant_client.get_collections()
    return 'Server Started successfully'


@app.route('/ingest/',methods=['GET'])
def ingestDoc():

    qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URI"), 
    api_key=os.getenv("QDRANT_API_KEY"),
    )
    loader = PyPDFLoader('./docs/aws-sdk-ref.pdf')
    print(len(loader))

if __name__=='__main__':
    app.run(debug=True)
    ingestDoc()
