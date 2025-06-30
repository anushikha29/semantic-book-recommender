# 📚 Semantic Book Recommender

A semantic, emotion-aware book recommender system using Hugging Face, LangChain, Gradio, and Transformers, allowing you to search, explore, and recommend books based on semantic similarity, categories, and emotions in their descriptions.

---

## 🚀 Features

- Semantic search over book descriptions
- Zero-shot classification to handle category gaps (~79% accuracy)
- Emotion detection on book descriptions for flexible filtering
- Vector database (Chroma) for fast retrieval
- Gradio interface for interactive exploration

---

## 🛠️ Tech Stack

- Python
- Hugging Face (Transformers, sentence-transformers)
- LangChain
- Chroma
- Gradio

---

## ⚡ Usage

1️⃣ Clone the repository:
```bash
git clone https://github.com/anushikha29/semantic-book-recommender.git
cd semantic-book-recommender
```
2️⃣ Install dependencies
```
pip install -r requirements.txt
```
3️⃣ Run the Gradio app
```
python gradio-dashboard.py
```

## 🙏 Acknowledgements
Special thanks to freeCodeCamp and the freeCodeCamp YouTube channel for their excellent and clear videos, which helped me understand and build this semantic recommender system effectively.