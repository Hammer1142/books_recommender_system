from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
from src.pipeline.recommend_pipeline import RecommendPipeline

application = Flask(__name__)

app = application
df_books_data = pd.read_csv("./data/processed/books_data_processed.csv")
books_data = df_books_data.to_dict(orient="records")
df_books_ratings = pd.read_csv("./data/processed/books_ratings_processed.csv")
books_ratings = df_books_ratings.to_dict(orient="records")
liked_books = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            liked_books.append(user_input)
    search_query = request.form.get('search', '')
    if search_query:
        filtered_df = df_books_data[df_books_data['Title'].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df_books_data
    return render_template('index.html', liked_books=liked_books, filtered_df=filtered_df.to_dict(orient='records'), search_query=search_query)





@app.route('/home')
def home():
    recommend_pipeline = RecommendPipeline(books_data=df_books_data, books_ratings=df_books_ratings, liked_books=liked_books)
    top_recs, popular_recs = recommend_pipeline.get_recommendations_based_on_ratings()
    top_recs_dict = top_recs.to_dict(orient="records")
    popular_recs_dict = popular_recs.to_dict(orient="records")
    return render_template('home.html', liked_books=liked_books, top_recs=top_recs_dict, popular_recs=popular_recs_dict)



"""@app.route('/search', methods=['POST'])
def search_books():
    query = request.json.get('query', '').lower()
    results = [book for book in books if query in book['content'].lower()]
    return jsonify(results)"""

@app.route("/book_list")
def book_list():
    return render_template("book_list.html", books=books_data)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)