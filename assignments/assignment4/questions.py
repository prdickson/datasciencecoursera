import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df = pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
mlb_df=pd.read_csv("assets/mlb.csv")
nfl_df=pd.read_csv("assets/nfl.csv")

cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

def nhl_correlation():

    def parseInt(v):
        try:
            return int(v)
        except ValueError:
            return None

    def parseTeam(t):
        reps = {
            'Tampa Bay': 'Tampa Bay Area',
            'Toronto Maple': 'Toronto',
            'New York': 'New York City',
            'New Jersey': 'New York City',
            'Washington': 'Washington, D.C.',
            'Anaheim': 'San Francisco Bay Area',
            'San Jose': 'San Francisco Bay Area',
            'Detroit Red': 'Detroit',
            'Columbus Blue': 'Columbus',
            'Minneapolis': 'Minneapolis–Saint Paul',
            'Florida': 'Miami–Fort Lauderdale',
            'Carolina': 'Raleigh',
            'Arizona': 'Phoenix',
            'Dallas': 'Dallas–Fort Worth',
            'Minnesota': 'Minneapolis–Saint Paul',
            'Colorado': 'Denver',
            'Vegas Golden': 'Las Vegas'
        }

        t = ' '.join(t.replace('*', '').split(' ')[:-1])
        return reps.get(t, t)

    global nhl_df
    nhl_df = nhl_df[nhl_df['year'] == 2018]
    nhl_df['W'] = nhl_df['W'].apply(parseInt)
    nhl_df['GP'] = nhl_df['GP'].apply(parseInt)
    nhl_df = nhl_df.dropna()
    nhl_df['team'] = nhl_df['team'].apply(parseTeam)

    nhl_df = pd.merge(nhl_df, cities, how='left', left_on='team', right_on='Metropolitan area')
    g = nhl_df.groupby('team').agg({'W': np.sum, 'GP': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / g['GP']
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g['ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    return stats.pearsonr(population_by_region, win_loss_by_region)


def nba_correlation():

    def parseInt(v):
        try:
            return int(v)
        except ValueError:
            return None

    def parseTeam(t):
        reps = {
            'Tampa Bay': 'Tampa Bay Area',
            'Toronto Maple': 'Toronto',
            'New York': 'New York City',
            'Brooklyn': 'New York City',
            'New Jersey': 'New York City',
            'Washington': 'Washington, D.C.',
            'Anaheim': 'San Francisco Bay Area',
            'Golden State': 'San Francisco Bay Area',
            'San Jose': 'San Francisco Bay Area',
            'Detroit Red': 'Detroit',
            'Columbus Blue': 'Columbus',
            'Minneapolis': 'Minneapolis–Saint Paul',
            'Florida': 'Miami–Fort Lauderdale',
            'Carolina': 'Raleigh',
            'Arizona': 'Phoenix',
            'Dallas': 'Dallas–Fort Worth',
            'Minnesota': 'Minneapolis–Saint Paul',
            'Colorado': 'Denver',
            'Vegas Golden': 'Las Vegas',
            'Portland Trail': 'Portland',
            'Miami': 'Miami–Fort Lauderdale',
            'Utah': 'Salt Lake City',
            'Indiana': 'Indianapolis',
        }

        t = ' '.join(t.replace('*', '').split(' ')[:-1])
        return reps.get(t, t)

    global nba_df
    nba_df = nba_df[nba_df['year'] == 2018]
    nba_df['W'] = nba_df['W'].apply(parseInt)
    nba_df['L'] = nba_df['L'].apply(parseInt)

    nba_df = nba_df.dropna()
    nba_df['team'] = nba_df['team'].apply(parseTeam)

    nba_df = pd.merge(nba_df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = nba_df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g['ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)


def mlb_correlation():

    def parseInt(v):
        try:
            return int(v)
        except ValueError:
            return None

    def parseTeam(t):
        reps = {
            'Tampa Bay': 'Tampa Bay Area',
            'Toronto Maple': 'Toronto',
            'Toronto Blue': 'Toronto',
            'New York': 'New York City',
            'Brooklyn': 'New York City',
            'New Jersey': 'New York City',
            'Washington': 'Washington, D.C.',
            'Anaheim': 'San Francisco Bay Area',
            'Golden State': 'San Francisco Bay Area',
            'San Jose': 'San Francisco Bay Area',
            'Oakland': 'San Francisco Bay Area',
            'San Francisco': 'San Francisco Bay Area',
            'Detroit Red': 'Detroit',
            'Columbus Blue': 'Columbus',
            'Minneapolis': 'Minneapolis–Saint Paul',
            'Florida': 'Miami–Fort Lauderdale',
            'Carolina': 'Raleigh',
            'Arizona': 'Phoenix',
            'Dallas': 'Dallas–Fort Worth',
            'Texas': 'Dallas–Fort Worth',
            'Minnesota': 'Minneapolis–Saint Paul',
            'Colorado': 'Denver',
            'Vegas Golden': 'Las Vegas',
            'Portland Trail': 'Portland',
            'Miami': 'Miami–Fort Lauderdale',
            'Utah': 'Salt Lake City',
            'Indiana': 'Indianapolis',
            'Boston Red': 'Boston',
            'Chicago White': 'Chicago',
            'Los Angeles Angels of': 'Los Angeles',
        }

        t = ' '.join(t.replace('*', '').split(' ')[:-1])
        return reps.get(t, t)

    global mlb_df
    mlb_df = mlb_df[mlb_df['year'] == 2018]
    mlb_df['W'] = mlb_df['W'].apply(parseInt)
    mlb_df['L'] = mlb_df['L'].apply(parseInt)

    mlb_df = mlb_df.dropna()
    mlb_df['team'] = mlb_df['team'].apply(parseTeam)

    mlb_df = pd.merge(mlb_df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = mlb_df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g['ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)


def nfl_correlation():
    def parseInt(v):
        try:
            return int(v)
        except ValueError:
            return None

    def parseTeam(t):
        reps = {
            'Tampa Bay': 'Tampa Bay Area',
            'New York': 'New York City',
            'Washington': 'Washington, D.C.',
            'San Francisco': 'San Francisco Bay Area',
            'Carolina': 'Charlotte',
            'Arizona': 'Phoenix',
            'Dallas': 'Dallas–Fort Worth',
            'Minnesota': 'Minneapolis–Saint Paul',
            'Miami': 'Miami–Fort Lauderdale',
            'New England': 'Boston',
            'Tennessee': 'Nashville',
            'Oakland': 'San Francisco Bay Area',
        }

        t = ' '.join(t.replace('*', '').split(' ')[:-1])
        return reps.get(t, t)

    global nfl_df
    nfl_df = nfl_df[nfl_df['year'] == 2018]
    nfl_df['W'] = nfl_df['W'].apply(parseInt)
    nfl_df['L'] = nfl_df['L'].apply(parseInt)

    nfl_df = nfl_df.dropna()
    nfl_df['team2'] = nfl_df['team']
    nfl_df['team'] = nfl_df['team'].apply(parseTeam)

    nfl_df = pd.merge(nfl_df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = nfl_df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g['ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)

