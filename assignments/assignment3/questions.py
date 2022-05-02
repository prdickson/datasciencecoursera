import pandas as pd
import numpy as np
import re
renames = {
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong",
    "Korea, Rep.": "South Korea",
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"
}


def rename_countries(c):
    c = c.split('(')[0].strip()
    c = re.sub('[0-9]', '', c)

    if c in renames:
        return renames[c]

    return c.split('(')[0].strip()


Energy = pd.read_excel('assets/Energy Indicators.xls', skiprows=17, nrows=227)

Energy = Energy.drop([Energy.columns[0], Energy.columns[1]], axis=1)
Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
Energy = Energy.replace('...', np.nan)
Energy['Energy Supply'] *= 1000000

Energy['Country'] = Energy['Country'].apply(rename_countries)

GDP = pd.read_csv('assets/world_bank.csv', skiprows=4)
GDP['Country'] = GDP['Country Name'].apply(rename_countries)

GDP = GDP[['Country', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
frames = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']


def a(x):
    return np.mean(x)

GDP['AVG'] = GDP[frames].apply(a, axis=1)
result_df = GDP.drop(frames,axis=1)
# print(result_df)



ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')
ScimEn = ScimEn[ScimEn['Rank'] <= 15]

def answer_one():

    m = pd.merge(ScimEn, Energy, how='inner', on='Country')
    m = pd.merge(m, GDP, how='inner', on='Country')
    m = m.set_index('Country')
    return m.sort_values('Rank')

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):

    def answer_three():
        m = answer_one()
        s = m[['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']].mean(axis=1)
        s.name = "avgGDP"
        return s.sort_values(ascending=False)


    def answer_four():
        m = answer_three()
        sixth_largest = m.keys()[5]

        top15 = answer_one()

        return top15.loc[sixth_largest]["2015"] - top15.loc[sixth_largest]["2006"]


    def answer_six():
        Top15 = answer_one()

        v = Top15.sort_values(by="% Renewable", ascending=False).iloc[0][["% Renewable"]]
        return (v.name, v.item())


    S = pd.Series(np.arange(5), index=['a', 'b', 'c', 'd', 'e'])

    print(S[1:4])
    print(S[S <= 3][S > 0])


    df = pd.DataFrame([[5,6,20],[2,82,28],[71,31,92],[67,37,49]], columns=['a','b','c'], index=['v','x', 'y', 'z'])

    f = lambda x: x.max() + x.min()
    df_new = df.apply(f)

    # print(df.pivot_table(['max', 'min']))

    multicol1 = pd.MultiIndex.from_tuples([('weight', 'kg'),
                                           ('weight', 'pounds')])
    df = pd.DataFrame([[1, 2], [2, 4]],
                                        index=['cat', 'dog'],
                                        columns=multicol1)

    print(df.unstack().unstack())
