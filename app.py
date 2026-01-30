"""Main flask app to serve book club site"""

import os
from flask import Flask, render_template

app = Flask(__name__)

app.config["FREEZER_RELATIVE_URLS"] = True


@app.route("/")
def index():
    """Serve up the home page"""
    return render_template("book_club_index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
