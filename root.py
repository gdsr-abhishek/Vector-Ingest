from flask import Flask
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
app = Flask(__name__)
load_dotenv()
@app.route('/',methods=['GET'])
def root():
    qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URI"), 
    api_key=os.getenv("QDRANT_API_KEY"),
    )
    return qdrant_client.get_collections()


@app.route('/ingest/',methods=['POST'])
def ingestDoc():

    qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URI"), 
    api_key=os.getenv("QDRANT_API_KEY"),
)

    print(qdrant_client.get_collections())


if __name__=='__main__':
    app.run(debug=True)
