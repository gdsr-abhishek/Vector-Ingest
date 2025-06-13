
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings ,ChatOpenAI
import numpy as np
from sklearn.manifold import TSNE
import plotly.graph_objects as go
from langchain_chroma import Chroma
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
print(f"{len(chunks)} chunks created")
embeddings=OpenAIEmbeddings()
if os.path.exists("aws"):
    Chroma(persist_directory="aws",embedding_function=embeddings).delete_collection()

vectorstore = Chroma.from_documents(documents=chunks,embedding=embeddings,persist_directory="aws")
print(f"Vectorstore created with {vectorstore._collection.count()} documents")

collection = vectorstore._collection
sample_embedding = collection.get(limit=1,include=["embeddings"])["embeddings"][0]
print(f"dimensions: {len(sample_embedding)}")
print(sample_embedding)