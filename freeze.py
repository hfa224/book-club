"""Uses flask freeze to generate static site files"""

from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

if __name__ == "__main__":
    print("Building website...")
    app.debug = False
    app.testing = True
    freezer.freeze()
