import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant

# load_dotenv()
# qdrant_api_key = os.getenv("API_KEY")
# qdrant_url = os.getenv("URL")

huggingface_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


qdrant_api_key = st.secrets["qdrant"]["API_KEY"]
qdrant_url = st.secrets["qdrant"]["URL"]

raw_documents = TextLoader("tagged_description.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=0, chunk_overlap=0, separator="\n")
documents = text_splitter.split_documents(raw_documents)

# Populate collection
db_books = Qdrant.from_documents(
    documents,
    embedding=huggingface_embeddings,
    url=qdrant_url,
    api_key=qdrant_api_key,
    collection_name="semantic-book-recommender",
    timeout=120
)

print("qdrant collection populated successfully.")
