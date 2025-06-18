from dotenv import load_dotenv
load_dotenv()
import json
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Updated imports
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Qdrant configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

def load_and_chunk_json(dir_path, chunk_size=1000, chunk_overlap=100):
    docs = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    for root, _, files in os.walk(dir_path):
        for fname in files:
            if fname.lower().endswith('.json'):
                path = os.path.join(root, fname)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for key, text in data.items():
                    full_text = f"{key}: {text}"
                    parts = splitter.split_text(full_text)
                    for i, chunk in enumerate(parts):
                        docs.append(
                            Document(
                                page_content=chunk,
                                metadata={
                                    "source_file": fname,
                                    "source_key": key,
                                    "chunk_index": i
                                }
                            )
                        )
    return docs

if __name__ == '__main__':
    docs = load_and_chunk_json('data/')
    # Ensure OPENAI_API_KEY is set in your environment
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-large",
        openai_api_key=OPENAI_API_KEY,
    )
    vectorstore = Qdrant.from_documents(
        docs,
        embeddings,
        url=QDRANT_URL,
        prefer_grpc=False,
        api_key=QDRANT_API_KEY,
        collection_name=QDRANT_COLLECTION_NAME,
        batch_size=20 ,
    )
    print(f"Indexed {len(docs)} chunks into Qdrant.")
