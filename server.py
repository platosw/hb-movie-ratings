"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    return render_template('homepage.html')


@app.route('/movies')
def show_movies():
   movies = crud.get_movies()
   return render_template('movies.html', movies=movies)


@app.route(f'/movies/<movie_id>')
def show_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_detail.html', movie=movie)


@app.route('/movies/<movie_id>', methods=["POST"])
def rating_score(movie_id):
    score = request.form.get("score")
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_email(session['user'])
    rating = crud.create_rating(score, movie, user)
    db.session.add(rating)
    db.session.commit()
    return redirect(f'/user_data/{user.user_id}')


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("users.html", users=users)


@app.route('/user_data/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template('user_data.html', user=user)


@app.route('/users', methods=["POST"])
def register_users():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    
    if user:
        flash('Your email is already exist. Try again.')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please Log in.')

    return redirect('/')

@app.route('/login', methods=["POST"])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)

    if user.password == password:
        session['user'] = user.email
        flash("You're logged in.")
    else:
        flash("You have wrong email or password. Try again.")

    return redirect('/')

@app.route('/logout')
def logout_user():
    session.clear()
    flash("You're logged out.")
    return redirect('/')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
