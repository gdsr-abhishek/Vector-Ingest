
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dotenv import load_dotenv
load_dotenv()
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URI"), 
    api_key=os.getenv("QDRANT_API_KEY"),
    )

loader = PyPDFLoader('./docs/aws-sdk-ref.pdf')
pages = loader.load()
for page in pages:
    page.metadata['doc_name']= 'aws-sdk-ref.pdf'

chunker = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
chunks= chunker.split_documents(pages)