import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
#%matplotlib inline


import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

#base_url = "https://sofifa.com/players?v=17&e=158837&set=true?offset="
offset = 0

columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club',
           'Club Logo', 'Value', 'Wage', 'Special']


e_values = ['158438','158410','158375','158347','158319','158284','158256','158227','158193','158166',
            '158131','158103']

data = DataFrame(columns=columns)
offset_url = "&offset="


for ur in e_values:
    full_player_data = 'full_player_data'+ur+'.csv'
    basicplayerdata  = 'basicplayerdata' + ur +'.csv'
    PlayerAttributeData = 'PlayerAttributeData'+ur+'.csv'
    Allplayer = 'Allplayer'+ur+'.csv'
    Dataset = 'Dataset'+ur+'.csv'

    base_u ='https://sofifa.com/player/'
    base_url = "https://sofifa.com/players?v=18&e=" + ur +"&set=true"+ offset_url

    for offset in range(255):
        url = base_url + str(offset*80)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        table_body = soup.find('tbody')
        counter = 0
        for row in table_body.findAll('tr'):
            td = row.findAll('td')
            picture = td[0].find('img').get('data-src')
            pid = td[0].find('img').get('id')
            nationality = td[1].find('a').get('title')
            flag_img = td[1].find('img').get('data-src')
            name = td[1].findAll('a')[1].text
            age = td[2].find('div').text.strip()
            overall = td[3].text.strip()
            potential = td[4].text.strip()
            club = td[5].find('a').text
            club_logo = td[5].find('img').get('data-src')
            value = td[7].text
            wage = td[8].text
            special = td[17].text
            player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall,
                                      potential, club, club_logo, value, wage, special]])
            player_data.columns = columns
            data = data.append(player_data, ignore_index=True)
            counter+=1
        offset+=1
        print(offset)
        data.to_csv(full_player_data, encoding='utf-8')

    data = pd.read_csv(full_player_data)
    #print(data)

    data.to_csv(basicplayerdata, encoding='utf-8')
    player_data_url = base_u
    r = 0
    for index, row in data.iterrows():
        skill_names = []
        skill_map = {'ID' : str(row['ID'])}
        url = player_data_url + str(row['ID'])
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        categories = soup.findAll('div', {'class': 'col-3'})
        for category in categories[:-1]:
            skills = category.findAll('li')
            for skill in skills:
                a = skill.text.split()
                a.reverse()
                value = a.pop()
                a.reverse()
                n = ' '.join(a)
                skill_names.append(n)
                skill_map[str(n)] = value
        master_data = DataFrame(columns=skill_names)
        break

    player_data_url = base_u
    r = 0
    for index, row in data.iterrows():
        skill_names = []
        skill_map = {'ID' : str(row['ID'])}
        url = player_data_url + str(row['ID'])
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        categories = soup.findAll('div', {'class': 'col-3'})
        for category in categories[:-1]:
            skills = category.findAll('li')
            for skill in skills:
                a = skill.text.split()
                a.reverse()
                value = a.pop()
                a.reverse()
                n = ' '.join(a)
                skill_names.append(n)
                skill_map[str(n)] = value
        attr_data = DataFrame(columns=skill_names)
        #print(attr_data)
        for key in skill_map.keys():
            attr_data.loc[r,key] = skill_map[key]
            #print(attr_data)
        r = r + 1
        print(r)
        master_data = pd.concat([master_data, attr_data])
        print(master_data)
        if r % 100 == 0:
            master_data.to_csv(PlayerAttributeData, encoding='utf-8')

    #print(master_data)
    full_data = pd.merge(data, master_data, left_index=True, right_index=True)

    full_data.to_csv(Allplayer, encoding='utf-8')
    master_data.to_csv(PlayerAttributeData, encoding='utf-8')
    full_data.to_csv(Dataset, encoding='utf-8')
    #print(full_data)
    full_data.drop('Unnamed: 0', 1,  inplace=True)
    #print(full_data)
    full_data.drop('ID_x', 1,  inplace=True)
    #print(full_data['ID_y'])
    f = full_data.rename(index=str, columns={"ID_y": "ID"})
    #print(f['ID'])
    f.to_csv(Dataset, encoding='utf-8')
    #print(f)
