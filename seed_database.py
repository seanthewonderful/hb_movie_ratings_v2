"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

movies = []

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
    
    for movie in movie_data:
        new_movie = crud.create_movie(title=movie['title'],
                                      overview=movie['overview'],
                                      release_date=datetime.strptime(movie['release_date'], "%Y-%m-%d"),
                                      poster_path=movie['poster_path'])
        movies.append(new_movie)
        
model.db.session.add_all(movies)
model.db.session.commit()

for n in range(1, 11):
    email = f"user{n}@test.com"
    password ="test"
    
    new_user = crud.create_user(email=email, password=password)
    model.db.session.add(new_user)
    
    for _ in range(10):
        rand_movie = choice(movies)
        rand_score = randint(1, 5)
        
        rating = crud.create_rating(user=new_user, 
                                    movie=rand_movie, 
                                    score=rand_score)
        model.db.session.add(rating)
    
model.db.session.commit()

    
    
    