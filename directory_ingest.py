import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from huggingface_hub import login
from kaggle_secrets import UserSecretsClient
from qdrant_client import QdrantClient,models
user_secrets = UserSecretsClient()
your_token = user_secrets.get_secret("HF_TOKEN") # Replace with your actual token
login(token=your_token)

path = '../input/jurisaidocs/jurisFiles'



qdrant_client = QdrantClient(
    url=user_secrets.get_secret("QDRANT_URL"), 
    api_key=user_secrets.get_secret('QDRANT_API_KEY'),
    )
qdrant_client.create_collection(
    collection_name="indJurisCollection",
    vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
)
files = os.listdir(path)
print(files)
# temp_file=[]
# temp_file.append(files[0])
# print(temp_file)
point_id = 1
for file in files:
    loader = PyPDFLoader(f"{path}/{file}")
    pages = loader.load()
    metadata = {}

    chunker = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    chunks=[]
    for page in pages:
        page.metadata['doc_name']= file
        chunk = chunker.split_text(page.page_content)
        chunks.extend(chunk)
        print("\n")
    model = SentenceTransformer('intfloat/e5-large-v2')
    embeddings=model.encode(chunks)
    
    print(embeddings)
    print(chunks)
    print(f"length of chunks: {len(chunks)} , length of embeddings: {len(embeddings)} ")
    embeddingPoints= []
    
    for chunk, embedding in zip(chunks,embeddings):
        point = models.PointStruct(
            id= point_id,
            payload={
                "fileName":str(file),
                "pageContent":chunk
            },
            vector = embedding
        )
        embeddingPoints.append(point)
        point_id+=1
    qdrant_client.upsert(
        
        collection_name= 'indJurisCollection',
        points= embeddingPoints
    )