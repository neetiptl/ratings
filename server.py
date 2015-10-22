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

    logged_in_user=User.query.filter(email==email, password==password).one()
    print logged_in_user

    if email == logged_in_user.email and password == logged_in_user.password:
        flash("user logged in")
        return redirect("") #FIX ME!!
    else:
        flash("wrong password or user not found")
        return redirect("/sign_in")

@app.route("/sign_out")
def sign_out():
    """ signs out user and redirects to homepage"""









    # # exists = None
    # if request.form('username'): #is in db:
    #     if request.form('password') == #id equal to username[password]
    #     else:
    #         flash("WRONG PASSWORD!")
    # else:
    #     flash("USER NOT FOUND. PLEASE REGISTER!")
    #     return render_template("/sign_in.html")
    # return redirect("/")


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