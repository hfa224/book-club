""" Contains methods to read book data from csv file"""

import csv
from datetime import datetime
import os
import requests
from typing import Dict


# cache for book cover urls to avoid repeatedly querying open covers
# to check if it has the book cover we want
book_cover_urls: Dict[str, str] = {}


def make_from_row(row):
    """Create a book dictionary from a row of the csv file"""

    rating = {"Helen": row[4], "Max": row[5], "Beth": row[6], "Average": row[8]}

    # check the cache first for this isbn
    if row[9] in book_cover_urls:
        # print("found " + row[9] + " in cache")
        cover_img = book_cover_urls[row[9]]
    else:
        cover_img = get_book_image_url(
            row[9]
        )  # "https://covers.openlibrary.org/b/isbn/"+ row[9] + "-M.jpg"
        book_cover_urls[row[9]] = cover_img

    return {
        "title": row[0],
        "author": row[1],
        "picker": row[2],
        "date": row[3],
        "genre": row[7],
        "cover_image_url": cover_img,
        "rating": rating,
    }


def get_book_image_url(isbn):
    """Get the book image url - first checks for local image, if unavailable will query openlibrary
    Finally will display a ??? image"""
    image_url = "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg"
    local_img_url = (
        "images/book_covers/" + isbn + ".png"
    )  # book cover images should by pngs named after the isbn

    if os.path.exists("static/" + local_img_url):
        return local_img_url
    try:
        if requests.head(url=image_url + "?default=false", timeout=10).status_code != 404:
            return image_url
    except requests.exceptions.Timeout:
        print("Cover image request to open library timed out - using default img")
    return "images/book_covers/mystery_book.png"  # if no cover image, return mystery book image


def read_book_isbns():
    """Get the book image url - first checks for local image, if unavailable will query openlibrary
    Finally will display a ??? image"""
    book_array = []
    with open(
        file="static/data/Berlin Beer & Book Club.csv", encoding="UTF-8"
    ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                book_array.append(make_from_row(list(row)))
    sorted_books = sorted(
        book_array,
        key=lambda book_dict: datetime.strptime(book_dict["date"], "%m-%Y").date(),
        reverse=True,
    )
    return sorted_books


def who_has_the_most_genres(book_array):
    """From the book_array, find the picker who has the most diverse genre selection"""
    books_by_picker = {}
    for book in book_array:
        picker = book["picker"]
        if picker not in books_by_picker:
            books_by_picker[picker] = set([])
        for split_genre in book["genre"].split("/"):
            books_by_picker[picker].add(split_genre)

    genres_dict = dict((k, len(v)) for k, v in books_by_picker.items())
    winner = max(genres_dict, key=genres_dict.get)
    return (
        winner,
        "you have the most diverse amount of genres with "
        + str(genres_dict.get(winner))
        + " genres!",
    )
