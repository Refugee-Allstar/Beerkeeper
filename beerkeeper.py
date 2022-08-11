from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import json
from types import SimpleNamespace

sc = OAuth2(None, None, from_file='./credentials.json')
gm = yfa.Game(sc, 'nfl')



def get_teams():
    lg = gm.to_league('406.l.477467')
    teams = lg.teams()
    all_names = []
    for key in lg.teams().keys():
        d={'Name':teams[key]['name']}
        all_names.append(d)
    return all_names

def get_rankings():
    lg = gm.to_league('406.l.477467')
    ranks = lg.standings()
    
    all_ranks = []
    for x in range(len(ranks)):
        d={'Name':ranks[x]['name'], 'Rank': ranks[x]['rank'], 'team_key':ranks[x]['team_key']}
        all_ranks.append(d)
    return all_ranks

def get_players():


    lg = gm.to_league('406.l.477467')
    ranks = lg.standings()
    
    top_roster = []
    first_place = lg.standings()[0]['team_key']

    tm = yfa.Team(sc, first_place)
    roster = tm.roster(16)
    for x in range(len(roster)):
        new = json.dumps(roster[x])
        test = json.loads(new, object_hook=lambda d: SimpleNamespace(**d))
        d={'name': test.name}
        top_roster.append(d)
    return top_roster

def past_ranks(year):
    year = str(year)
    try:
        league = gm.league_ids(year=year)
        if year == '2016':
            lg = gm.to_league(league[1])
        if year == '2017':
            lg = gm.to_league(league[1])
        else:
            lg = gm.to_league(league[0])
        ranks = lg.standings()
        all_ranks = []
        for x in range(len(ranks)):
            d={'Name':ranks[x]['name'], 'Rank': ranks[x]['rank'], 'team_key':ranks[x]['team_key']}
            all_ranks.append(d)
        return all_ranks
    except:
        return None

print(past_ranks(2018))