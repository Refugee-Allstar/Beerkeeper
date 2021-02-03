import pandas as pd
from tmdbv3api import TMDb, Movie, TV
import json
import requests

#https://api.themoviedb.org/3/movie/157336/watch/providers?api_key=f10fc84c1aff3f4baaa8d2328a5f21f3&append_to_response=videos,images
movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'f10fc84c1aff3f4baaa8d2328a5f21f3'


#https://api.themoviedb.org/3

def popular():
    popular = movie.popular()
    popular_movies = []
    for p in popular:
        movie_videos = movie.videos(p.id)
        movie_id = "NOT_FOUND"
        if movie_videos:
            movie_id = movie_videos[0]['key']
        d = {'Name': p.title, 'Rating': p.vote_average, 'Release Date': p.release_date, 'Description' : p.overview, 
        'Poster': p.poster_path, 'Popularity': p.popularity, 'Movie ID': movie_id, 'Vote Count' : p.vote_count, 'Movie TMDB ID': p.id,
        'Provider': 'cool'
        }
        popular_movies.append(d)

    return popular_movies[:8]

def get_provider(movie_id):
    d = requests.get('https://api.themoviedb.org/3/movie/'+movie_id+'/watch/providers?api_key='+tmdb.api_key+'&language=en-US')
    d_new = d.json() 
    
    rental = d_new['results']['US']['rent']
    for logo in rental:
        print(logo['logo_path'])


movie.recommendations

#print(popular_movies())
#print(movie.credits('775996'))


#d = movie.details('775996')
#for i in d['casts']['cast']:
#    print(i['name'])











