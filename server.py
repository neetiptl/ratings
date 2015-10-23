"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)

@app.route("/users/<int:user_id>") # how to use backref
def user_info(user_id):
    """ displaying user user info"""

    user = User.query.get(user_id)
    print user

    for rating in user.ratings:
        print rating.movie




    # test = Rating.query.filter(Rating.user.user_id==user_id).all()
    # print test

    # # user_info = Rating.query.filter_by(user_id=user_id).all()
    # print user_info
    # user_id_info = User.query.filter(user_id == user_id).first()
    # score = user_id_info.ratings
    # print score

    # return render_template("user.html", user_email = user_id_info.email, user_zip = user_id_info.zipcode)
    return redirect("/")    


@app.route("/register", methods = ['GET'])
def registration_form():
    """Display empty registration form"""

    return render_template("registration_form.html")



@app.route("/register", methods=['POST'])
def get_registration_data():
    """Collecting user entered data."""

    password = request.form.get('password')
    email = request.form.get('email')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    print email
    ##FIXME -make sure email isn't already in users
    current_user = User(password=password, age=age,email=email,zipcode=zipcode)
    db.session.add(current_user)

    db.session.commit()    

    return redirect("/")


@app.route("/sign_in")
def sign_in_form():
    """show sign in form to user"""

    return render_template("sign_in.html")


@app.route("/sign_in", methods=['POST'])
def get_sign_in_data():
    """collecting existing users login"""

    email = request.form.get("email")
    password = request.form.get("password")

    logged_in_user=User.query.filter_by(email=email, password=password).one()
    if logged_in_user:
        message = email + " logged in"
        flash(message)
        session['logged_in_user']=email
        return redirect("/") #FIX ME!!
    else:
        message = "wrong password or user not found"
        flash(message)
        return redirect("/sign_in")

@app.route("/sign_out")
def sign_out():
    """ signs out user and redirects to homepage"""
    # if session['logged_in_user']: ##FIXME if user isnt signed in, dont try to sign out/delete session
    del session['logged_in_user']

    return redirect("/")


@app.route("/logged_in")
def logged_in_user():
    """Allows logged in user to return to the home page"""

    username = session.get('username')
    password = session.get('password')
    flash
    return render_template('logged_in_user.html', username=username, password=password)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()