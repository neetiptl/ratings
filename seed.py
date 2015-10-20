"""Utility file to seed ratings database from MovieLens data in seed_data/"""


from model import User, Movie, Rating
# from model import Rating
# from model import Movie

from model import connect_to_db, db
from server import app

from datetime import datetime

def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row_splitted = row.split("|")
        ##throwing out rows with no release date or title is unknown
        
        movie_id = row_splitted[0]
        title = row_splitted[1]
        released_at = row_splitted[2]
        imdb_url = row_splitted[4]
        
        title_noyear = title.rstrip("(")
        if released_at != (''):
            released_at_ob = datetime.strptime(released_at, '%d-%b-%Y')
        else:
            pass
    

        movie = Movie(movie_id=movie_id,
                    title=title_noyear,
                    released_at=released_at_ob,
                    imdb_url=imdb_url)

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

    # Once we're done, we should commit our work
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Rating.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()
        print row
        row_splitted=row.split()
        user_id = row_splitted[0]
        movie_id = row_splitted[1]
        score = row_splitted[2]

        rating = Rating(movie_id=movie_id,
                    user_id=user_id,
                    score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)


    # Once we're done, we should commit our work
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
