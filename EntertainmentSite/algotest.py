# collaborative filter w implicit categorization, 2D embedding

# convert API dataset into matrix and categorize based on genre, director, user ratings?, 
# or convert into 2-4 matrixs, one for genre, director, length? 
# uses cosine similarity


import os
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from scipy.sparse import csr_matrix




TMDB_API_KEY = os.getenv("TMDB_API_KEY")



#### load dataset from TMDb, preprocess? turn into DB

dataset = None  

ds_movies = dataset['movieId']
ds_ratings = dataset['ratings']

# DATASET STATS 

n_movies = None #how many do we want to load? 200-300?
n_ratings = None
n_users = None #how many users?

print(f"Number of ratings: {n_ratings}")
print(f"Number of unique movieId's: {n_movies}")
print(f"Number of unique users: {n_users}")
print(f"Average ratings per user: {round(n_ratings/n_users, 2)}")
print(f"Average ratings per movie: {round(n_ratings/n_movies, 2)}")

user_freq = ds_ratings[['userId', 'movieId']].groupby('userId').count().reset_index()   #need subsections of dataset that gives us user ratings of movies
user_freq.columns = ['userId', 'n_ratings']


mean_rating = ds_ratings.groupby('movieId')[['rating']].mean()

l_rating = mean_rating['rating'].idxmin()
ds_movies.loc[ds_movies['movieId']==l_rating]

h_rating = mean_rating['rating'].idxmax()
ds_movies.loc[ds_movies['movieId']==h_rating]

print(ds_ratings[ds_ratings['movieId']==h_rating])
print(ds_ratings[ds_ratings['movieId']==l_rating])

movie_stats = ds_ratings.groupby('movieId')
[['rating']].agg['count', 'mean']
movie_stats.columns = movie_stats.columns.droplevel()




#creates matrixs to gauge simularity 
def create_matrix(df):
    N = len(df['userId'].unique())
    M = len(df['movieId'].unique())

    #maps ids to indices
    user_Mapper = dict(zip(np.unique(df['userId']), list(range(N))))
    movie_Mapper = dict(zip(np.unique(df['movieId']), list(range(M))))
    
    #maps indices to IDs
    user_inv_mapper = dict(zip(list(range(N))))


    #THERE IS MORE, THIS IS NOT FINISHED -- FOLLOWING EXAMPLE 



