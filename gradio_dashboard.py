import gradio as gr
import pandas as pd
from semantic_recs import recommend_books

books = pd.read_csv("books_with_emotions.csv")

categories = ["All"] + sorted(books["simple_categories"].unique())
tones = ["All"] + ["Happy", "Surprising", "Angry", "Suspenseful", "Sad", "Disturbing"]

with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
    gr.Markdown("# Semantic Book Recommender")

    with gr.Column():
        user_query = gr.Textbox(label= "Please enter a descriptoin of a book:",
                                placeholder= "e.g. A story about forgiveness")
        
        category_dropdown = gr.Dropdown(choices=categories,label="Select a category:", value="All")
        tone_dropdown = gr.Dropdown(choices=tones,label="Select an emotional tone:", value="All")
        submit_button = gr.Button("Find Recommendation")


        gr.Markdown("## Recommendations")
        output = gr.Gallery(label = "Recommend books", columns = 8, rows = 2)

        submit_button.click(fn = recommend_books,
                            inputs=[user_query,category_dropdown,tone_dropdown],
                            outputs=output)


if __name__ == "__main__":
    dashboard.launch()
