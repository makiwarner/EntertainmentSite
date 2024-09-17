# pip install Flask requests
# mkdir flask_tmdb
# cd flask_tmdb
# New-Item app.py -ItemType File

# basic route to make API requests

from flask import Flask, jsonify, request, render_template
import requests
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL= "https://api.themoviedb.org/3"


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/movie/info_similar')
def get_movie_info_similar():
    query = request.args.get('query')
    search_url= f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"

    search_response = requests.get(search_url)
    search_data = search_response.json()

    if search_data['results']:
        movie_id = search_data['results'][0]['id']
        movie_url = f'{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}'
        movie_response = requests.get(movie_id)
        movie_metadata = movie_response.json()

        similar_url = f"{BASE_URL}/movie/{movie_id}/similar?api_key={TMDB_API_KEY}"
        similar_response = requests.get(similar_url)
        similar_movies = similar_response.json()['results'][:5]

        return jsonify({
            "movie_metadata": movie_metadata,
            "similar_movies": similar_movies
        })  
    
    else:
        return jsonify({"error": "Movie not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)  



