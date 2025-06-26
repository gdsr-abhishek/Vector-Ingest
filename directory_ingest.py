import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
path = './jurisFiles'
files = os.listdir(path)
print(files)
for file in files:
    loader = PyPDFLoader(f"{path}/{file}")
    pages = loader.load()
    metadata = {}

    chunker = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks=[]
    for page in pages:
        page.metadata['doc_name']= file
        chunk = chunker.split_text(page.page_content)
        chunks.append(chunk)
    model = SentenceTransformer('intfloat/e5-large-v2')
    embeddings=model.encode(chunks)
    print(embeddings)