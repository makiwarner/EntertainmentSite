#

from flask import Flask, jsonify, request, render_template
import requests
import os
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL= "https://api.themoviedb.org/3"

db = mysql.connector.connect( 
    host=os.getenv("MYSQL_HOST"),
    user= os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),  
    database= os.getenv("MYSQL_DATABASE")
)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/movie/info_similar', methods=['GET'])
def get_movie_meta_similar():
    query= request.args.get('query')
    search_url= f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if search_data['results']:
        movie_id=search_data['results'][0]['id']
        similar_url= f"{BASE_URL}/movie/{movie_id}/similar?api_key={TMDB_API_KEY}"
        similar_response= requests.get(similar_url)
        similar_movies =similar_response.json()['results'][:50]

        #stores in the mysql db
        cursor = db.cursor()
        for movie in similar_movies:
            cursor.execute("""
                INSERT INTO movies (id, title, overview, release_date, poster_path)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title=VALUES(title), overview=VALUES(overview), release_date=VALUES(release_date), poster_path=VALUES(poster_path)
            """, (movie['id'],movie['title'], movie['overview'],movie['release_date'], movie['poster_path']))
        db.commit()


        return jsonify(similar_movies)
    else:
        return jsonify({"error": "Movie not found"}), 404
    


@app.route('/movies')
def get_stored_movies():
    cursor= db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    movies= cursor.fetchall()
    return render_template('movies.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)