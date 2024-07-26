import csv
import requests
import os

from datetime import datetime

# cache for book cover urls to avoid repeatedly querying open covers
# to check if it has the book cover we want
book_cover_urls = {}


class Book:
    def __init__(self, title, author, picker, date, genre, cover_image_url, rating):
        self.title = title
        self.author = author
        self.picker = picker
        self.date = date
        self.genre = genre
        self.cover_image_url = cover_image_url
        self.rating = rating

    def make_from_row(row):

        rating = {"Helen": row[4], "Max": row[5], "Beth": row[6], "Average": row[8]}

        #print(book_cover_urls.keys())

        # check the cache first for this isbn
        if row[9] in book_cover_urls.keys():
            #print("found " + row[9] + " in cache")
            cover_img = book_cover_urls[row[9]]
        else:
            cover_img = get_book_image_url(row[9])  # "https://covers.openlibrary.org/b/isbn/"+ row[9] + "-M.jpg"
            book_cover_urls[row[9]] = cover_img

        return Book(row[0], row[1], row[2], row[3], row[7], cover_img, rating)


def read_book_data():
    with open("static/data/Berlin Beer & Book Club.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{row[2]} picked {row[0]} by {row[1]} in {row[3]}.')
                line_count += 1
        # print(f'Processed {line_count} lines.')


def get_book_image_url(isbn):
    image_url = "https://covers.openlibrary.org/b/isbn/" + isbn + "-M.jpg"
    local_img_url = "images/book_covers/" + isbn + ".png"  # book cover images should by pngs named after the isbn
    
    if os.path.exists("static/" + local_img_url):
        return local_img_url
    elif requests.head(image_url + "?default=false").status_code != 404:
        return image_url
    else:
        return "images/cb08c741ede41b10539c45ac96f7b05c.gif"# just a place holder....


def read_book_isbns():
    book_array = []
    with open("static/data/Berlin Beer & Book Club.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                book_array.append(Book.make_from_row(row))
    sorted_books = sorted(
        book_array,
        key=lambda x: datetime.strptime(x.date, "%m-%Y").date(),
        reverse=True,
    )
    return sorted_books

def who_has_the_most_genres(book_array):
    picked_books = sort_books_by_picker(book_array)
    genres = {}
    for key, value in picked_books.items():
        genres[key] = get_all_genres(value)

    highest_number_of_genres = max(genres.values(), key=lambda genre_list: genre_list.size())
    return sorted_books

def sort_books_by_picker(book_array):
    return {book.picker:book for book in book_array}

def get_all_genres(book_list):
    genres = []
    for genre in map(lambda x: x.genre, book_array):
        for split_genre in genre.split("/"):
            genres.append(split_genre)
    return genres
