import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as file:
    movie_data = json.loads(file.read())
    
movies_in_db = []
for movie in movie_data:
    title = movie["title"]
    overview = movie["overview"]
    poster_path = movie["poster_path"]

    date_str = movie["release_date"]
    format = "%Y-%m-%d"
    release_date = datetime.strptime(date_str, format)

    new_movie = crud.create_movie(title, overview, release_date, poster_path)
    movies_in_db.append(new_movie)
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    new_user = crud.create_user(email, password)
    model.db.session.add(new_user)

    for _ in range(10): #꼭!!! 질문할 것!!!
        score = randint(1, 5)
        movie = choice(movies_in_db)
        new_rating = crud.create_rating(score, movie, new_user)
        model.db.session.add(new_rating)


model.db.session.commit()
