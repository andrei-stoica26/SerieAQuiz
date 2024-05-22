import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import os

def save_players_data(url, active_players):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[0]
    table_html = str(table)
    table_io = StringIO(table_html)
    dfs = pd.read_html(table_io)
    df = dfs[0]
    if not os.path.exists('Data'):
        os.makedirs('Data')
    df = df[~df['Player'].isin(active_players)]
    df = df.drop(['Rank', 'Notes'], axis = 1)
    df.to_csv('Data/serieadata.csv')

def main():
    url = 'https://en.wikipedia.org/wiki/List_of_Serie_A_players_with_100_or_more_goals'
    active_players = ['Ciro Immobile',
                  'Paulo Dybala',
                  'Domenico Berardi',
                  'Duván Zapata',
                  'Dries Mertens',
                  'Edinson Cavani',
                  'Andrea Belotti',
                  'Edin Džeko',
                  'Lautaro Martínez',
                  'Luis Muriel']
    save_players_data(url, active_players)

if __name__=='__main__':
    main()
