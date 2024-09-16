from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Home route
@app.route('/home')
def home():
    return render_template('home.html')

# For now, adding "/find-similar" will simply return the searched movie. 
# It is this way just to verify a connection to the DB is successfully established.
# I will later update the queries to find a SIMILAR movie to the one searched.
@app.route('/find-similar', methods=['GET', 'POST'])
def find_similar():
    if request.method == 'POST':
        search_query = request.form['search']
        category = request.form['category']  # options = movie, show, book, or all

        conn = sqlite3.connect('/Users/makennawarner/FlaskProject/Sept_13/EntertainmentSite/recommendation.sqlite')
        cursor = conn.cursor()

        recommendations = []
        if category == 'movie' or category == 'all':
            cursor.execute("SELECT * FROM Movies WHERE title LIKE ?", ('%' + search_query + '%',))
            recommendations += cursor.fetchall()
        
        if category == 'show' or category == 'all':
            cursor.execute("SELECT * FROM Shows WHERE title LIKE ?", ('%' + search_query + '%',))
            recommendations += cursor.fetchall()
        
        if category == 'book' or category == 'all':
            cursor.execute("SELECT * FROM Books WHERE title LIKE ?", ('%' + search_query + '%',))
            recommendations += cursor.fetchall()

        conn.close()
        return render_template('find_similar.html', recommendations=recommendations, search_query=search_query)
    
    return render_template('find_similar.html', recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
