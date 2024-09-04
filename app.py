""" Main flask app to serve book club site """

import os
from datetime import datetime
from flask import Flask, render_template
from encrypt_flask_template import encrypt
from read_data import read_book_isbns, who_has_the_most_genres

app = Flask(__name__)

app.config["FREEZER_RELATIVE_URLS"] = True


@app.route("/")
def home():
    """Serve up the home page"""
    book_array = read_book_isbns()

    current_book = max(
        book_array, key=lambda book: datetime.strptime(book["date"], "%m-%Y").date()
    )
    book_array.remove(current_book)
    return render_template(
        "book_club.html", book_array=book_array, current_book=current_book
    )


@app.route("/book_club_about/")
def book_club_about():
    """Serve up the about page"""
    return render_template("book_club_about.html")

@app.route("/book_club_wrapped/")
def wrapped():
    """Serve up the wrapped page"""
    # create a list of tuples
    members_list = [
        ("M_ENCRYPTED_PAYLOAD", book_club_wrapped("Max"), "max2024"),
        ("B_ENCRYPTED_PAYLOAD", book_club_wrapped("Beth"), "beth2024"),
        ("H_ENCRYPTED_PAYLOAD", book_club_wrapped("Helen"), "helen2024"),
    ]
    return encrypt(members_list)


def book_club_wrapped(name):
    """Generate book club wrapped page from template"""
    book_array = read_book_isbns()
    winner = []
    if name in who_has_the_most_genres(book_array):
        winner.append(who_has_the_most_genres(book_array))

    picked_books = [x for x in book_array if x["picker"].strip() == name.strip()]
    # we need to filter dnfs out here
    highest_rated_book = max(book_array, key=lambda book: book["rating"][name] if book["rating"][name] != "dnf" else "0")
    highest_rated_picked_book = max(
        picked_books, key=lambda book: book["rating"]["Average"]
    )
    genres = []
    for genre in map(lambda x: x["genre"], book_array):
        for split_genre in genre.split("/"):
            genres.append(split_genre)

    return render_template(
        "book_club_wrapped.html",
        book_array=book_array,
        picked_books=picked_books,
        name=name,
        highest_rated_book=highest_rated_book,
        highest_rated_picked_book=highest_rated_picked_book,
        genres=genres,
        winner=winner,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
