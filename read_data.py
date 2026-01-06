"""Contains methods to read book data from csv file"""

import csv
from datetime import datetime
import os
import calendar
from typing import Dict, List
import re

# remember the picker order
picker_order: List = ["Max", "Beth", "Helen"]

def make_from_row(row):
    """Create a book dictionary from a row of the csv file"""
    rating = {"Helen": row[4], "Max": row[5], "Beth": row[6], "Average": row[8]}

    cover_img = get_book_image_url(row[0], row[1])

    return {
        "title": row[0],
        "author": row[1],
        "picker": row[2],
        "date": row[3],
        "genre": row[7],
        "cover_image_url": cover_img,
        "rating": rating,
    }


def get_book_image_url(title, author):
    """Get the book image url - first checks for local image, if not present will display a ??? image"""

    title_and_author = title + "_" + author
    title_and_author_underscore = re.sub(' ', '_', title_and_author)
    url_string_sanitised = re.sub(r'\W+', '', title_and_author_underscore).lower()


    local_img_url = (
        "images/book_covers/" + url_string_sanitised + ".jpg"
    )  # book cover images should by jpgs named after the isbn

    print(url_string_sanitised)

    if os.path.exists("static/" + local_img_url):
        return local_img_url
    return "images/book_covers/mystery_book.jpg"  # if no cover image, return mystery book image


def read_book_isbns():
    """Get the book image url - first checks for local image, if unavailable will query openlibrary
    Finally will display a ??? image"""
    book_array = []
    with open(
        file="static/data/book_data.csv", encoding="UTF-8"
    ) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # ignore the header row
                line_count += 1
            elif len(row) > 0:  # only add row if not empty
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

def who_has_the_highest_rated(book_array):
    """Find the picker who picked the highest rated book"""

    max_rating_book = max(book_array, key=lambda book: book["rating"]["Average"])


    winner = max_rating_book["picker"]
    return (
        winner,
        "you have the highest rated book, "
        + str(max_rating_book["title"])
        + " with a rating of " + str(max_rating_book["rating"]["Average"])
    )


def generate_next_pick_message(current_book):
    """Generate the message to show who picks the next book and when"""
    # we need to know who picked the last book and the month it was picked
    picker = current_book["picker"]
    date = datetime.strptime(current_book["date"], "%m-%Y").date()

    current_month_index = datetime.now().date().month
    month_index = (date.month + 1) % 12
    # if we've run over (i.e. we've skipped a month), just say we'll pick in the current month
    print(month_index)
    print(current_month_index)
    month_index = max(month_index, current_month_index)

    index = (picker_order.index(picker) + 1) % 3

    return (
        "The next book will be picked by "
        + picker_order[index]
        + " in "
        + calendar.month_name[month_index]
        + "."
    )
