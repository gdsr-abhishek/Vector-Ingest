
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
# print(sample_embedding)
result = collection.get(include=["embeddings","documents","metadatas"])
vectors= np.array(result["embeddings"])
documents = result["documents"]
tsne= TSNE(n_components=2 , random_state=42)
rv= tsne.fit_transform(vectors)
fig = go.Figure(data=[go.Scatter(
x=rv[:,0],
y=rv[:,1],
mode="markers",
  marker=dict(size=5, opacity=0.8),
 text=[f"<br>Text: {d[:100]}..." for  d in documents],
 hoverinfo='text'
)])
fig.update_layout(
    title='2D Chroma Vector Store Visualization',
    scene=dict(xaxis_title='x',yaxis_title='y'),
    width=800,
    height=600,
    margin=dict(r=20, b=10, l=10, t=40)
)
fig.show()