# 📚 Semantic Book Recommender

A semantic, emotion-aware book recommender system using Hugging Face, LangChain, Gradio, Streamlit and Transformers, allowing you to search, explore, and recommend books based on semantic similarity, categories, and emotions in their descriptions.

---

## 🚀 Features

- Semantic search over book descriptions
- Zero-shot classification to handle distinct and missing categories (~79% accuracy)
- Emotion detection on book descriptions for flexible filtering
- Vector database (Qdrant) for fast retrieval
- Gradio interface for interactive exploration
- Streamlit Deployment 

---

## 🛠️ Tech Stack

- Python
- Hugging Face (Transformers, sentence-transformers)
- LangChain
- Qdrant Cloud
- Gradio (initial)
- Streamlit (current)

---

## ⚡ Usage [(🌐 Live Project)](https://semantic-book-recommender.streamlit.app)

1️⃣ Clone the repository:
```bash
git clone https://github.com/anushikha29/semantic-book-recommender.git
cd semantic-book-recommender
```
2️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 📺 Run Locally
Gradio:
```
python gradio-dashboard.py
```
![image](https://github.com/user-attachments/assets/d9261f31-b704-4a14-97fb-35529b3da178)

Streamlit:
```
streamlit run app.py
```
![image](https://github.com/user-attachments/assets/9e6a2f34-11cd-490e-871a-f804a56efc61)

## 🌱 Future Improvements
✨ I plan to continue improving this project by adding personalized reading analytics, smarter emotion-based recommendations, and collaborative book club features in the future.

## 🙏 Acknowledgements
Special thanks to freeCodeCamp and the freeCodeCamp YouTube channel for their excellent and clear videos, which helped me understand and build this semantic recommender system effectively.
