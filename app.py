import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

from semantic_recs import retrieve_semantic_recs

google_creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
google_creds = json.loads(google_creds_json)


# ---- custom css ----
def local_css():
    st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #6c63ff;
        color: white;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #5750e3;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ---- Lottie Loader Function ----
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

book_lottie = load_lottieurl("https://lottie.host/944c515c-388b-488a-98d0-7698316553a2/rtwz5tnyH2.json")

# ---- Sidebar Navigation ----
st.sidebar.title("📚 Semantic Book Recommender")
page = st.sidebar.radio("Navigation", ["Home", "About", "Usage"])

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Anushikha")

# ---- Home Page ----
if page == "Home":
    st.title("📚 Semantic Book Recommender")
    st_lottie(book_lottie, height=180, key="book")

    st.write("Discover books based on **meaning, mood, and themes**, not just titles or authors.")

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        description = st.text_area(
            "📝 Describe the book you want to find:",
            placeholder="e.g. A story about resilience, adventure, and finding one's true path.",
            height=120
        )
    with col2:
        category = st.selectbox(
            "🏷️ Category:",
            ["All", "Fiction", "Non-Fiction", "Children's Nonfiction", "Children's Fiction"]
        )
        emotion = st.selectbox(
            "💫 Emotional Tone:",
            ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad", "Disturbing"]
        )
    top_k = st.slider(
        "📊 Recommendations:",
        min_value=1,
        max_value=15,
        value=5,
        key="top_k_slider",
        help="Select how many books you want to see in the recommendations.",
    )


    st.markdown("---")
    center_button = st.columns([1, 2, 1])[1]
    with center_button:
        find_rec = st.button("🚀 Find Recommendations", use_container_width=True)

    if find_rec:
        if description.strip() == "":
            st.warning("Please enter a book description to get recommendations.")
        else:
            with st.spinner("🔍 Finding the best book recommendations for you..."):
                try:
                    results = retrieve_semantic_recs(
                        query=description,
                        category=None if category == "All" else category,
                        tone=None if emotion == "All" else emotion,
                        final_top_k=top_k
                    )
                    st.success("✨ Here are your recommended books:")

                    for idx, row in results.iterrows():
                        with st.expander(f"📖 {row['title']} — *{row['authors']}*"):
                            cols = st.columns([1, 3])
                            with cols[0]:
                                image_url = row["thumbnail"] if pd.notna(row["thumbnail"]) else "https://via.placeholder.com/150"
                                st.image(image_url, use_container_width=True)
                            with cols[1]:
                                st.markdown(f"**📘 Title:** {row['title']}")
                                st.markdown(f"**✍️ Author(s):** {row['authors']}")
                                st.markdown(f"**🏷️ Category:** {row['simple_categories']}")
                                st.markdown(f"**📖 Pages:** {int(row['num_pages']) if pd.notna(row['num_pages']) else 'N/A'}")
                                st.markdown(f"**⭐ Rating:** {row['average_rating']}/5")
                                st.markdown(f"**📅 Year:** {int(row['published_year']) if pd.notna(row['published_year']) else 'N/A'}")
                                if pd.notna(row['description']):
                                    st.markdown(f"**📝 Description:** {row['description'][:600]}{'...' if len(row['description']) > 600 else ''}")
                                else:
                                    st.markdown("_No description available._")
                                st.markdown(f"[🔗 View on Goodreads](https://www.goodreads.com/search?q={row['title'].replace(' ', '+')})")

                    csv = results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Recommendations as CSV",
                        data=csv,
                        file_name='recommended_books.csv',
                        mime='text/csv',
                    )
                except Exception as e:
                    st.error(f"❌ An error occurred: {e}")

# ---- About Page ----
elif page == "About":


    google_creds = st.secrets["google"]

    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
    client = gspread.authorize(creds)


    sheet = client.open("Fable user accounts").sheet1
    
    st.title("📖 About Semantic Book Recommender")
    st_lottie(book_lottie, height=180, key="about")

    st.markdown("""
Welcome to **Semantic Book Recommender**, an intelligent tool designed to help you discover books based on **meaning, mood, and themes** and built straight from the heart of an avid reader 💛

### 🚀 Why Did I Build This Project?
Ever since I can remember, books have been more than just stories — they’ve been a source of comfort, adventure, and a way of understanding life.  
As a reader myself, I’ve often wished for recommendations that *understood* what I was truly in the mood for — whether something emotionally rich, suspenseful, or full of joy.
This project was my way of combining that love for literature with my passion for technology.  
It uses advanced **natural language processing**, **semantic search**, **emotion detection**, and **zero-shot classification** to suggest books not just based on genre — but based on **feeling** ✨.
Traditional book recommendation engines often overlook your current emotions or the deeper themes you wish to explore. This tool uses **semantic embeddings, vector databases, and NLP** to find books that align with your current mindset, making your reading journey more personal and meaningful.

### 🛠️ Tech Stack:
- Python
- LangChain
- Hugging Face Transformers
- Qdrant Cloud (Vector DB)
- Gradio(Initial) and Streamlit(current)
- [Kaggle dataset](https://www.kaggle.com/datasets/dylanjcastillo/7k-books-with-metadata)
                
---
### 📚 Let’s Connect on Fable!
If you're on **Fable**, let’s share recommendations, join book clubs, and read together 🌼

- 🔗 [Visit My Fable Profile](https://fable.co/nova-335730351344)
- 📬 Or drop your Fable account below and I'll connect with you!

""")
    user_fable = st.text_input("Your Fable username or profile link:")

    if st.button("📬 Submit"):
        if user_fable.strip() != "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, user_fable])
            st.success(f"📩 Thanks! I’ll check out **{user_fable}** and connect with you on Fable soon 💌")
        else:
            st.warning("Please enter your Fable username or link before submitting.")


    st.markdown("""
---        
### 🎓 Credits:
This project was inspired by **freeCodeCamp’s Semantic Book Recommender video**, and utilizes open tools provided by **Hugging Face and LangChain** to make advanced NLP accessible for practical projects.

### 📂 [View on GitHub](https://github.com/anushikha29/semantic-book-recommender)
                
##### Future updates will bring even smarter, personalized recommendations and book club features. Stay tuned!
---

Made with ❤️ by **Anushikha**.
""")

# ---- Usage Page ----
elif page == "Usage":
    st.title("📘 How to Use")
    st.markdown("""
1️⃣ **Enter a Description:**  
Describe the type of book you want to find (themes, mood, keywords).

2️⃣ **Select Category & Emotion:**  
Optionally filter by category and emotional tone.

3️⃣ **Adjust Results:**  
Choose the number of recommendations you want.

4️⃣ **Find Recommendations:**  
Click the button, and you'll receive books matching your criteria.

5️⃣ **Download Recommendations:**  
Save the recommendations as a CSV for future reading plans.

---

Enjoy your personalized reading journey! 🚀
""")
