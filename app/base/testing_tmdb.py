import pandas as pd
from requests.api import get
from tmdbv3api import TMDb, Movie, TV
import json
import requests
import itertools

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
    d = movie.release_dates(movie_id) 
    #print(json.dumps(d_new, indent=2))
    release = d['results']
    for i in release:
        if i['iso_3166_1'] == "US":
            release_dates = i['release_dates']
            for j in release_dates:
                platforms = []
                for n in release_dates:
                    if n['note']:
                        platforms.append(n['note'])
                    else:
                        pass
                return platforms
        else:
            pass
        #print(i)
        #print(i['iso_3166_1'])

    #for logo in rental:
    #    print(logo['logo_path'])




#print(popular_movies())
#print(movie.credits('775996'))


#d = movie.details('464052')
#print(d)
#for i in d['casts']['cast']:
#    print(i['name'])

#get_provider('464052')

print(get_provider('464052'))


#print(movie.release_dates('775996'))



<form class="navbar-left navbar-form nav-search mr-md-3" aria-expanded="true" role="form" method="post" action="">
{{ form.hidden_tag() }}
    {% if msg %}
        {{ msg | safe }}
    {% endif %}                     
<div class="input-group">
{{ form.movie(placeholder="Search For Movies", class="form-control") }}
    <div class="input-group-prepend">
        <button type="submit" class="btn btn-search pr-1">
            <i class="fa fa-search search-icon"></i>
        </button>
    </div>
</form>