# flake8: noqa

from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os




env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


pdf_path=Path(__file__).parent/"nodejs.pdf"

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

print (f"Total pages: {len(docs)}")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200,
)

split_docs = text_splitter.split_documents(docs)

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
   
)

vector_store =QdrantVectorStore.from_documents(
    documents=split_docs,
    collection_name="vector_learning",
    url="http://vector-db:6333",
    embedding=embeddings,
)

print("Documents added to vector store successfully!")