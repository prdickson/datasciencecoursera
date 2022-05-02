import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df = pd.read_csv("assets/nhl.csv")
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

print(nhl_correlation())

# with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
    #     print(g)
    #     print(g.shape)

