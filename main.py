from flask import Flask, request
from google.cloud import datastore

MOVIES = 'movies'
MSG_ATTRIBUTES_ERROR = {"Error": "The request body is missing at least one of the required attributes"}
NO_MOVIE_FOUND_ERROR = {"Error": "No movie with this movie_id exists"}

app = Flask(__name__)
client = datastore.Client()

@app.route('/')
def index():
    return "Jello World! This is the library search and filter microservice. Authors: Urbano San Roman, Gurveer, Samual"

def has_all_necessary_data_for_movie(movie):
    """
    movie is a json/dict object.
    returns True if all necessary attributes are in data
    """
    attributes = movie.keys()
    result = ('title' in attributes) and \
    ('year' in attributes) and \
    ('genre' in attributes) and \
    ('director' in attributes) and \
    ('description' in attributes) and \
    ('rating' in attributes)

    return result

@app.route('/' + MOVIES, methods = ['POST'])
def post_movie():
    # get content of request
    content = request.get_json()

    # create key for the kind, "MOVIE"
    movie_key = client.key(MOVIES)

    # create entity/document using newly created key. update document using request contents
    new_movie = datastore.Entity(key = movie_key)
    if has_all_necessary_data_for_movie(content):
        new_movie.update({
            'title':content['title'],
            'year': content['year'],
            'genre': content['genre'],
            'director': content['director'],
            'description': content['description'], 
            'rating':content['rating']
        })
        client.put(new_movie)

        # fetch id of new movie entity
        new_movie['id'] = new_movie.key.id
        return(new_movie, 201)
    else:
        return(MSG_ATTRIBUTES_ERROR, 400)

@app.route('/' + MOVIES, methods = ['GET'])
def get_all_movies():
    # fetch movies from datastore. define query
    query = client.query(kind = MOVIES)
    result = list(query.fetch())                # fetch is a query method. use the query method 'fetch' to return the list of movies

    # add movie id to each of the movies before returning result
    for movie in result:
        movie['id'] = movie.key.id
    
    return result

@app.route('/' + MOVIES + '/<int:id>', methods = ['GET'])
def get_a_movie_by_id(id):
    movie_key = client.key(MOVIES, id)
    movie = client.get(movie_key)
    if movie is None:
        return(NO_MOVIE_FOUND_ERROR, 404)
    else:
        movie['id'] = movie.key.id
        return(movie)

@app.route('/' + MOVIES + '/<int:id>', methods = ['PUT'])
def edit_a_movie(id):
    movie_key = client.key(MOVIES, id)
    movie = client.get(movie_key)
    if movie is None:
        return(NO_MOVIE_FOUND_ERROR, 404)

    content = request.get_json()
    if has_all_necessary_data_for_movie(content):
        movie.update({
            'title':content['title'],
            'year': content['year'],
            'genre': content['genre'],
            'director': content['director'],
            'description': content['description'],
            'rating': content['rating']
        })
        client.put(movie)
        movie['id'] = movie.key.id
        return movie
    else:
        return(MSG_ATTRIBUTES_ERROR, 400)
    
@app.route('/' + MOVIES + '/<int:id>', methods = ['DELETE'])
def delete_a_movie(id):
    movie_key = client.key(MOVIES, id)
    movie = client.get(movie_key)
    if movie is None:
        return (NO_MOVIE_FOUND_ERROR, 404)
    
    client.delete(movie_key)
    return ('', 204)

# @app.route('/owners/<int:owner_id>/businesses', methods = ['GET'])
# def list_all_businesses_for_owner(owner_id):
#     # get query parameters from request
#     query = client.query(kind = BUSINESSES)
#     all_businesses = list(query.fetch())
#     result = []
#     for biz in all_businesses:
#         if biz['owner_id'] == owner_id:
#             biz['id'] = biz.key.id
#             result.append(biz)
#     return result
















if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)

