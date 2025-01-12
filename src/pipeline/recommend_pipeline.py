import sys
import pandas as pd
from src.exception import CustomException

class RecommendPipeline:
    def __init__(self, books_data, books_ratings, liked_books):
        self.books_data = books_data
        self.books_ratings = books_ratings
        self.liked_books = liked_books
        self.similar_users = set()
        self.recs_lines = []
        
    def check_for_similar_users(self, row):
        if str(row["book_id"]) in self.liked_books and row["review/score"] >= 4:
            self.similar_users.add(row["User_id"])
            
    def check_for_recs(self, row):
        if row["User_id"] in self.similar_users and str(row["book_id"]) not in self.liked_books:
            self.recs_lines.append([row["User_id"], row["book_id"], row["review/score"]])
    
    def get_recommendations_based_on_ratings(self):
        self.books_ratings.apply(self.check_for_similar_users, axis=1)
        self.books_ratings.apply(self.check_for_recs, axis=1)
        #self.books_data["book_id"] = self.books_data["book_id"].astype(str)
        recs = pd.DataFrame(self.recs_lines, columns=["User_id", "book_id", "review/score"])
        recs["book_id"] = recs["book_id"].astype(str)
        #get top 20 recs?
        top_recs = recs["book_id"].value_counts().head(20)
        top_recs_id = top_recs.index.values
        top_recs_list = top_recs_id.tolist()
        top_recs_list = [int(x) for x in top_recs_list]
        top_recs = self.books_data[self.books_data['book_id'].isin(top_recs_list)]
        all_recs = recs["book_id"].value_counts()     
        all_recs = all_recs.to_frame().reset_index()     
        #self.books_data["book_id"] = self.books_data["book_id"].astype(str)
        all_recs["book_id"] = all_recs["book_id"].astype(int)
        all_recs = all_recs.merge(self.books_data, how="inner", on="book_id")
        print(f"Al3: {all_recs}; Type: {type(all_recs)}")        
        all_recs.drop(columns=["index"], inplace=True)
        all_recs.rename(columns={"count":"recommended_count"}, inplace=True)
        all_recs["score"] = all_recs["recommended_count"] * (all_recs["recommended_count"] / all_recs["rating_count"])
        popular_recs = all_recs[all_recs["rating_count"] > 100].sort_values("score", ascending=False).head(20)
        return top_recs, popular_recs
    
    
    def get_recommendations_based_on_description():
        pass
    
    def get_recommendations_based_on_category():
        pass