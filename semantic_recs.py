import pandas as pd
import numpy as np

from langchain_community.document_loaders import TextLoader # raw text will get converted into a format that langchain can work with
from langchain_text_splitters import CharacterTextSplitter #will split all the descriptions into meaningful chunks
from langchain_community.embeddings import HuggingFaceEmbeddings #converting the chunks into document embeddings
from langchain_qdrant import Qdrant #storing them in a vector database
from dotenv import load_dotenv
import streamlit as st
import os

tone_mapping = {
    "Happy": "joy",
    "Surprising": "surprise",
    "Angry": "anger",
    "Suspenseful": "fear",
    "Sad": "sadness",
    "Disturbing": "digust"
}


# load_dotenv()
# qdrant_api_key = os.getenv("API_KEY")
# qdrant_url = os.getenv("URL")

huggingface_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

qdrant_api_key = st.secrets["qdrant"]["API_KEY"]
qdrant_url = st.secrets["qdrant"]["URL"]

books= pd.read_csv("books_with_emotions.csv")

books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"

books["large_thumbnail"] = books["thumbnail"].fillna("").apply(
    lambda x: x + "&fife=w800" if x.strip() != "" else "no-cover-found.jpg"
)

raw_documents = TextLoader("tagged_description.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=0, chunk_overlap=0, separator="\n")
documents = text_splitter.split_documents(raw_documents)

db_books = Qdrant.from_existing_collection(
    collection_name="semantic-book-recommender",
    embedding=huggingface_embeddings,
    url=qdrant_url,
    api_key=qdrant_api_key,
)

def retrieve_semantic_recs(
    query: str,
    category: str = None,
    tone: str = None,
    initial_top_k: int = 150,
    final_top_k: int = 50,
) -> pd.DataFrame:
    """
    Retrieves semantic book recommendations, with optional filtering and sorting.
    """
    if not query or not isinstance(query, str) or query.strip() == "":
        return pd.DataFrame()
    
    recs = db_books.similarity_search(query, k=initial_top_k)

    if not recs:
        st.warning("No semantic matches found for your query. Try a broader query.")
        return pd.DataFrame()

    
    books_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    book_recs = books[books["isbn13"].isin(books_list)]

    if category and category != "All":
        book_recs = book_recs[book_recs["simple_categories"] == category]

    if tone and tone != "All":
        emotion_column = tone_mapping.get(tone)
        if emotion_column and emotion_column in book_recs.columns:
            book_recs = book_recs[book_recs[emotion_column] > 0]
            book_recs = book_recs.sort_values(by=emotion_column, ascending=False)


    book_recs = book_recs.head(final_top_k)

    if book_recs.empty:
        st.warning(
            "No books matched your specific filters. Showing top semantic matches instead."
        )
        book_recs = books[books["isbn13"].isin(books_list)].head(final_top_k)

    return book_recs

def recommend_books(
        query: str,
        category: str,
        tone: str
):
    recommendations = retrieve_semantic_recs(query, category, tone)
    results = []

    for _, row in recommendations.iterrows():
        description = row["description"]
        truncated_desc_split = description.split()

        truncated_description = " ".join(truncated_desc_split[:30])+ "..."

        authors_split = row["authors"].split('"')
        if len(authors_split) ==2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) >2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = row["authors"]


        caption = f"{row['title']} by {authors_str}: {truncated_description}"
        results.append((row["large_thumbnail"], caption))
    return results

categories = ["All"] + sorted(books["simple_categories"].unique())
tones = ["All"] + ["Happy", "Surprising", "Angry", "Suspenseful", "Sad", "Disturbing"]
