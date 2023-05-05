from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    user = User(email=email, password=password)
    return user

def get_users():
    return User.query.all()

def get_user_by_id(id):
    return User.query.get(id)

def get_user_by_email(emailData):
    return User.query.filter_by(email=emailData).first() # 이 코드는 값이 없으면 None을 반환한다.


def create_movie(title, overview, release_date, poster_path):
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    return movie

def get_movies():
    return Movie.query.all()

def get_movie_by_id(id):
    return Movie.query.get(id)

def create_rating(score, movie, user):
    rating = Rating(score=score, movie=movie, user=user)
    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
