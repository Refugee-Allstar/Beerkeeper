# -*- encoding: utf-8 -*-

from typing import NewType
import requests
from app.home import blueprint
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import pandas as pd
from tmdbv3api import TMDb, Movie, TV
from app.base.forms import LoginForm, CreateAccountForm, MovieForm
import json
import app

movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'f10fc84c1aff3f4baaa8d2328a5f21f3'



#def get_actors(movie_id):
#    actors = movie.credits(movie_id)
#    actor_list = []
#   for a in actors:
@blueprint.route('/item/update', methods=['PUT'])        
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']


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
                    try:
                        if n['note']:
                            platforms.append(n['note'])
                            return {'Networks': platforms, 'Logo': 'N/A'}
                    except:
                        return {'Networks': 'KODI', 'Logo': 'N/A'}
                else:
                    pass


def rent_services(movie_id):
    d = requests.get('https://api.themoviedb.org/3/movie/'+movie_id+'/watch/providers?api_key='+tmdb.api_key+'&language=en-US')
    d_new = d.json()
    rent_services = []
    try: 
        for i in d_new['results']['US']['rent']:
            data = {'Networks': i['provider_name'], 'Logo': i['logo_path']}
            rent_services.append(data)
        return rent_services
    except:
        try:
            new_dict = d_new['results']['US']['flatrate'][0]
            for i in new_dict:
                data = {'Networks': i['provider_name'], 'Logo': i['logo_path']}
                rent_services.append(data)
            return rent_services 
        except:
                return {'Networks': 'N/A', 'Logo': 'N/A'}
def popular():
    popular = movie.popular()
    popular_movies = []
    for p in popular:
        network = get_provider(str(p.id))
        if not network:
            network = rent_services(str(p.id))
        print(p.id, p.title, network)
        movie_videos = movie.videos(p.id)
        movie_id = "NOT_FOUND"
        if movie_videos:
            movie_id = movie_videos[0]['key']
        d = {'Name': p.title, 'Rating': p.vote_average, 'Release Date': p.release_date, 'Description' : p.overview, 
        'Poster': p.poster_path, 'Popularity': p.popularity, 'Movie ID': movie_id, 'Vote Count' : p.vote_count, 'Movie TMDB ID': p.id,
        'Provider_Info': network
        }
        popular_movies.append(d)

    return popular_movies[:8]

def find_movie(movie_name):
    request = movie.search(movie_name)
    final_result = []
    for r in request:
        network = get_provider(str(r.id))
        if not network:
            network = rent_services(str(r.id))
        movie_videos = movie.videos(r.id)
        movie_details = movie.details(r.id)
        movie_id = "NOT_FOUND"
        try:
            release_date = r.release_date
        except:
            release_date = "UNKNOWN"
        if movie_videos:
            movie_id = movie_videos[0]['key']
        d = {'Name': r.title, 'Rating': r.vote_average, 'Release Date': release_date, 'Description' : r.overview, 
        'Poster': r.poster_path, 'Popularity': r.popularity, 'Movie ID': movie_id, 'Vote Count' : r.vote_count,
        'Revenue': movie_details['revenue'], 'Provider_Info': 'network'
        }
        print(d)
        final_result.append(d)
    return final_result



@blueprint.route('/', methods=['GET', 'POST'])

def index():
    popular_movies = popular()
    movie_form = MovieForm(request.form)
    if 'movie' in request.form:
        # read form data
        movie = request.form['movie']
        final_result = find_movie(movie)
        if not final_result:
            return render_template( 'index.html', msg = "No Movies Found With that Name Please Try Again", form=movie_form, popular = popular_movies)
        return render_template( 'index.html', result = final_result, form=movie_form, popular = popular_movies, api_key=tmdb.api_key)
    return render_template( 'index.html',
                                form=movie_form, popular = popular_movies)


@blueprint.route('/<template>')

def route_template(template):
    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/clear.html', methods=['GET', 'POST'])

def clear():
    session.clear()
    login_form = LoginForm(request.form)
    
    return render_template( 'login.html',
                                form=login_form)

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  


