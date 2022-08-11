# -*- encoding: utf-8 -*-

from typing import NewType
import requests
from app.home import blueprint
from flask import render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
import pandas as pd
from app.base.forms import LoginForm, CreateAccountForm, MovieForm
import json
import app
from beerkeeper import get_players, get_rankings, get_teams
all_teams = get_teams()
ranks = get_rankings()
winroster = get_players()

@blueprint.route('/item/update', methods=['PUT'])        
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']




@blueprint.route('/', methods=['GET', 'POST'])

def index():

    return render_template('index.html',beerteam=all_teams, ranking=ranks, top_roster=winroster, segment='index')



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


