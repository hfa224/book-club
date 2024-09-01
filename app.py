from flask import Flask, render_template
from read_data import read_book_data, read_book_isbns, who_has_the_most_genres
import os
from datetime import datetime

app = Flask(__name__)

app.config['FREEZER_RELATIVE_URLS']= True


@app.route("/")
def home():
    read_book_data()
    book_array = read_book_isbns()

    current_book = max(book_array, key=lambda book: datetime.strptime(book.date, "%m-%Y").date())
    book_array.remove(current_book)
    return render_template('book_club.html', book_array=book_array, current_book=current_book)

@app.route('/book_club_about/')
def book_club_about():
    return render_template('book_club_about.html')

# This is a noddy way of making the site able to be made static
@app.route('/book_club_wrapped/max/')
def wrapped_max():
    return book_club_wrapped("Max")

@app.route('/book_club_wrapped/beth/')
def wrapped_beth():
    return book_club_wrapped("Beth")

@app.route('/book_club_wrapped/helen/')
def wrapped_helen():
    return render_template('helen_pw_protected.html')
    #return book_club_wrapped("Helen")

def book_club_wrapped(name):
    book_array = read_book_isbns()
    winner = []
    if name in who_has_the_most_genres(book_array):
        winner.append(who_has_the_most_genres(book_array))
    
    picked_books = [x for x in book_array if x.picker.strip() == name.strip()]
    highest_rated_book = max(book_array, key=lambda book: book.rating[name])
    highest_rated_picked_book = max(picked_books, key=lambda book: book.rating["Average"])
    genres = []
    for genre in map(lambda x: x.genre, book_array):
        for split_genre in genre.split("/"):
            genres.append(split_genre)
    return render_template('book_club_wrapped.html', book_array=book_array, picked_books=picked_books, name=name, 
                           highest_rated_book=highest_rated_book, highest_rated_picked_book=highest_rated_picked_book, genres=genres,
                           winner=winner)

@app.route('/<string:name>/book_club_stats/')
def book_club_stats(name):
    book_array = read_book_isbns()
    picked_books = [x for x in book_array if x.picker.strip() == name.strip()]
    highest_rated_book = max(book_array, key=lambda book: book.rating[name])
    highest_rated_picked_book = max(picked_books, key=lambda book: book.rating["Average"])
    return render_template('book_club_stats.html', book_array=book_array, picked_books=picked_books, name=name, 
                           highest_rated_book=highest_rated_book, highest_rated_picked_book=highest_rated_picked_book)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))