import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df = pd.read_csv("assets/nhl.csv")
nba_df = pd.read_csv("assets/nba.csv")
mlb_df = pd.read_csv("assets/mlb.csv")
nfl_df = pd.read_csv("assets/nfl.csv")

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

    df = nhl_df[nhl_df['year'] == 2018].copy()
    df['W'] = df['W'].apply(parseInt)
    df['L'] = df['L'].apply(parseInt)
    df = df.dropna()
    df['team'] = df['team'].apply(parseTeam)

    df = pd.merge(df, cities, how='left', left_on='team', right_on='Metropolitan area')
    g = df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g[
        'ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


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

    df = nba_df[nba_df['year'] == 2018].copy()
    df['W'] = df['W'].apply(parseInt)
    df['L'] = df['L'].apply(parseInt)

    df = df.dropna()
    df['team'] = df['team'].apply(parseTeam)

    df = pd.merge(df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g[
        'ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


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

    df = mlb_df[mlb_df['year'] == 2018].copy()
    df['W'] = df['W'].apply(parseInt)
    df['L'] = df['L'].apply(parseInt)

    df = df.dropna()
    df['team'] = df['team'].apply(parseTeam)

    df = pd.merge(df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g[
        'ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


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

    df = nfl_df[nfl_df['year'] == 2018].copy()
    df['W'] = df['W'].apply(parseInt)
    df['L'] = df['L'].apply(parseInt)

    df = df.dropna()
    df['team2'] = df['team']
    df['team'] = df['team'].apply(parseTeam)

    df = pd.merge(df, cities, how='left', left_on='team', right_on='Metropolitan area')

    g = df.groupby('team').agg({'W': np.sum, 'L': np.sum, 'Population (2016 est.)[8]': np.max})
    g['ratio'] = g['W'] / (g['W'] + g['L'])
    g['Population (2016 est.)[8]'] = g['Population (2016 est.)[8]'].astype(float)

    population_by_region = g['Population (2016 est.)[8]']  # pass in metropolitan area population from cities
    win_loss_by_region = g[
        'ratio']  # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

print(nhl_correlation())
print(mlb_correlation())
print(nba_correlation())
print(nfl_correlation())
