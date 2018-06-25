#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
=Get Players' Data=
Scrapes all of the players' urls to get individual data from each one.
"""

import selenium_func as sel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helper_functions import read_from_file, append_to_file, process_info, append_to_csv

import time
import bs4
import ast

"""
Path where players urls are stored
"""
PLAYERS_URLS = 'players_urls/players_urls_complete.txt'

"""
Path to save players' data
"""
PLAYERS_DATA = 'players_data/players_data.txt'
"""
Path to save logs
"""
LOGS = 'players_data/players_data_logs.txt'
"""
Path to save searched teams.
"""
SEARCHED_TEAMS = 'searched_teams.txt'
"""
Path to save the main finished dataset. Without extension!
"""
DATASET = 'all_players_data'
"""
Features we want to extract.
"""
FEATURES = ['Player Name', #Get from url
            'Goals/90min','Assists/90min','Yel/90min','Red/90min','SpG','PS%','Rating', #Summary
            'Tackles','Inter','Fouls (def)','Offsides','Clear','DrB (def)','Blocks', #Defensive
            'DrB (off)','Fouled (off)', 'Off (off)', 'Disp (off)', #Offensive
            'KeyP','AvgP','Crosses','LongB','ThrB', #Passing
            'OutOfBox','SixYardBox','PenaltyArea', #Detailed
            'Playing Positions (Position-Apps-Goals-Assists-Rating)', 'Strengths',
            'Weaknesses', 'Style of Play'] 

"""
Functions
""" 

def get_players_data(first_idx, second_idx, players_urls, data, logs_path):
    """
    Get players' data and store it in a csv.
    =Args=
        players_urls: List with players' urls
        data_path: Path to save players' data
        errors_path: Path to save errors
        searched_teams: Path to save searched teams
    """
    
    server, driver = sel.start_server_and_driver()
    teams_players = read_from_file(players_urls)
                    
    teams_len = len(teams_players)-1
    table_names = ['summary','defensive','offensive','passing','detailed']
    
    for idx_1 in range(first_idx, teams_len): #type(players_urls) == list
        
        item = teams_players[idx_1]
        
        item_dict = ast.literal_eval(item)
                    
        for team, players in item_dict.items(): #string with team name, list with players' urls
            
            players_len = len(players)-1
                    
            for idx_2 in range(second_idx, 1):
                
                player = players[idx_2]
                #player = '/Players/11119/Show/Lionel-Messi'
                separated = player.split("Show")
                                
                for url_completion in ["History"]:
                    player = url_completion.join(separated)
                                
                    repeat = True
                    repeat_count = 10
                        
                    while repeat == True and repeat_count > 0:
                        
                        error = False
                        
                        processed = process_info(player)
                        
                        try:
                            complete_url = sel.WHOSCORED_URL + processed
            
                            try:
                                driver.get(complete_url)
                                
                            except Exception as e:
                                print('\n')
                                print("Problem accessing {}".format(processed))
                                print(str(e))
                                print('\n')
                                append_to_file("\nError accessing: " + processed + "\n", logs_path)
                                append_to_file("Index: " + str(teams_players.index(item)) + ", " + str(players.index(player)), logs_path)
                                append_to_file("Count: " + str(repeat_count), logs_path)
                                repeat_count -= 1
                                continue
                                    
                            player_name = ' '.join(processed.split('/')[-1].split('-'))
                            
                            #Save here the pre-parsed tables
                            player_tables = []
                    
                            #Iterate through table_names to get the html of each table
                            #If a table is not found, append "Undefined"
                            for table_name in table_names:
                                try:
                                    #Select a tag of table, to click it and get the html
                                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='#player-tournament-stats-" + table_name + "']")))
                                    driver.execute_script("arguments[0].click();", element)
                                    time.sleep(2)
                                except Exception as e:
                                    
                                    print(str(e))
                                    player_tables.append('Undefined')
                                    continue
                                
                                content = driver.page_source
                                soup = bs4.BeautifulSoup(''.join(content), 'lxml')
                                
                                try:
                                    #Get the table with the data
                                    stats_table = soup.find("div", {"id": "statistics-table-" + table_name }).find("tbody", {"id": "player-table-statistics-body"})
                                    player_tables.append(stats_table)
                                except Exception as e:
    
                                    player_tables.append('Undefined')
                                    continue
                                
                                    
                            #Undefined tables for when a table or data point is not found
                            undefined_tables = [['Undefined'] * 8, ['Undefined'] * 7, ['Undefined'] * 4,
                                                ['Undefined'] * 5, ['Undefined'] * 3]
                            
                            #Save here the data of this individual. player_data is a list of lists
                            player_data = []
                            #Parsing of the tables
                            for index in range(len(player_tables)):
                                #Table that we are going to parse
                                table = player_tables[index]
                                table_name = table_names[index]
                                #Undefined table
                                undefined_table = undefined_tables[index]
                                #If there is no table, then add a series of Undefineds to players_data
                                if table == 'Undefined':
                                    player_data += undefined_table
                                    continue
                                    
                                try:
                                    if 'Show' in player:
                                        trs = [table.find_all('tr')[-1]]
                                    else:
                                        trs = table.find_all('tr')[:-1]
                                        
                                except Exception:
                                    player_data += undefined_table
                                    continue
                                
                                for tr in trs:
                                    
                                    tds = tr.find_all('td')
                                   
                                    #Extract all the data from the tables
                                    if table_name == 'summary':
                                        if len(tds) != 12:
                                            player_data += undefined_table
                                        else:
                                            
                                            #Get the current season and name
                                            if 'Show' in player:
                                                season = "current"
                                            else:
                                                season = process_info(tds[0].get_text().strip())
                                            
                                            undefined_table[0] = player_name + "-" + season
                            
                                            mins = float(process_info(tds[2].get_text().strip())) if tds[2].get_text().strip() != '-' else "Undefined" #Mins
                                            if mins == "Undefined":
                                                undefined_table[1],undefined_table[2],undefined_table[3],undefined_table[4]=\
                                                ('Undefined','Undefined','Undefined','Undefined')
                                            else:
                                                goals = tds[3].get_text().strip()
                                                undefined_table[1] = str(round(float(goals)*90/mins,2))\
                                                                                if  goals != '-' else "Undefined" #Goals/90min
                                                assists = tds[4].get_text().strip()
                                                undefined_table[2] = str(round(float(assists)*90/mins,2))\
                                                                                if  assists != '-' else "Undefined" #Assists/90min
                                                yel = tds[5].get_text().strip()
                                                undefined_table[3] = str(round(float(yel)*90/mins,2))\
                                                                                if  yel != '-' else "Undefined" #Yel/90min
                                                red = tds[6].get_text().strip()
                                                undefined_table[4] = str(round(float(red)*90/mins,2))\
                                                                            if  red != '-' else "Undefined" #Red/90min
                                            spg = tds[7].get_text().strip()
                                            undefined_table[5] = process_info(spg) if  spg != '-' else "Undefined" #SpG
                                            
                                            ps = tds[8].get_text().strip()
                                            undefined_table[6] = process_info(ps) if  ps != '-' else "Undefined" #PS%
                                            
                                            rating = tds[11].get_text().strip()
                                            undefined_table[7] = process_info(rating) if  rating != '-' else "Undefined" #Rating
                                            
                                            player_data += undefined_table
                                    elif table_name == 'defensive':
                                        if len(tds) != 12:
                                            player_data += undefined_table
                                        else:
                                            tackles = tds[3].get_text().strip()
                                            undefined_table[0] = process_info(tackles) if tackles != '-' else "Undefined" #Tackles
                                            
                                            inter = tds[4].get_text().strip()
                                            undefined_table[1] = process_info(inter) if inter != '-' else "Undefined" #Inter
                                            
                                            fouls = tds[5].get_text().strip()
                                            undefined_table[2] = process_info(fouls) if fouls != '-' else "Undefined" #Fouls (def)
                                            
                                            offsides = tds[6].get_text().strip()
                                            undefined_table[3] = process_info(offsides) if offsides != '-' else "Undefined" #Offsides
                                            
                                            clear = tds[7].get_text().strip()
                                            undefined_table[4] = process_info(clear) if clear != '-' else "Undefined" #Clear
                                            
                                            drb = tds[8].get_text().strip()
                                            undefined_table[5] = process_info(drb) if drb != '-' else "Undefined" #Drb (def)
                                            
                                            blocks = tds[9].get_text().strip()
                                            undefined_table[6] = process_info(blocks) if blocks != '-' else "Undefined" #Blocks
                                            
                                            player_data += undefined_table
                                    elif table_name == 'offensive':
                                        if len(tds) != 13:
                                            player_data += undefined_table
                                        else:
                                            drb = tds[7].get_text().strip()
                                            undefined_table[0] = process_info(drb) if drb != '-' else "Undefined" #Drb (Off)
                                            
                                            fouled = tds[8].get_text().strip()
                                            undefined_table[1] = process_info(fouled) if fouled != '-' else "Undefined" #Fouled (Off)
                                            
                                            off = tds[9].get_text().strip()
                                            undefined_table[2] = process_info(off) if off != '-' else "Undefined" #Off (off)
                                            
                                            disp = tds[10].get_text().strip()
                                            undefined_table[3] = process_info(disp) if disp != '-' else "Undefined" #Disp (off)
                                            
                                            player_data += undefined_table
                                    elif table_name == 'passing':
                                        if len(tds) != 11:
                                            player_data += undefined_table
                                        else:
                                            keyp = tds[4].get_text().strip()
                                            undefined_table[0] = process_info(keyp) if keyp != '-' else "Undefined" #KeyP
                                            
                                            avgp = tds[5].get_text().strip()
                                            undefined_table[1] = process_info(avgp) if avgp != '-' else "Undefined" #AvgP
                                            
                                            crosses = tds[7].get_text().strip()
                                            undefined_table[2] = process_info(crosses) if crosses != '-' else "Undefined" #Crosses
                                            
                                            longb = tds[8].get_text().strip()
                                            undefined_table[3] = process_info(longb) if longb != '-' else "Undefined" #LongB
                                            
                                            thrb = tds[9].get_text().strip()
                                            undefined_table[4] = process_info(thrb) if thrb != '-' else "Undefined" #ThrB
                                            
                                            player_data += undefined_table
                                    elif table_name == 'detailed':
                                        if len(tds) != 8:
                                            player_data += undefined_table
                                        else:
                                            outofbox = tds[4].get_text().strip()
                                            undefined_table[0] = process_info(outofbox) if outofbox != '-' else "Undefined" #OutOfBox
                                            
                                            sixyardbox = tds[5].get_text().strip()
                                            undefined_table[1] = process_info(sixyardbox) if sixyardbox != '-' else "Undefined" #SixYardBox
                                            
                                            penaltyarea = tds[6].get_text().strip()
                                            undefined_table[2] = process_info(penaltyarea) if penaltyarea != '-' else "Undefined" #PenaltyArea
                                            
                                            player_data += undefined_table
                                            
                                
                            if 'Show' in player:
                                #Get Playing Positions, strengths, and weaknesses
                                
                                for search_item in [{"id": "player-positional-statistics" },
                                                    {"class": "strengths"},
                                                    {"class": "weaknesses"}]:
                                    
                                    try:
                                        tbody = soup.find("div", search_item).find("tbody")
                                        trs = tbody.find_all("tr")
                                        
                                        complete_list = []
                                        for tr in trs:
                                            partial_list = []
                                            tds = tr.find_all("td")
                                            for td in tds:
                                                td_text = td.get_text().strip()
                                                partial_list.append(process_info(td_text))
                                            complete_list.append("-".join(partial_list))
                                        
                                        if len(complete_list) == 0:
                                            player_data += ["Undefined"]
                                        else:
                                            player_data += ["/".join(complete_list)]
                                        
                                    except Exception:
                                        player_data += ["Undefined"]
             
                                #Get Style of Play
                                try:
                                    style = soup.find("div", {"class": "style"})
                                    lis = style.find_all("li")
                                    
                                    complete_list = []
                                    for li in lis:
                                        li_text = li.get_text().strip()
                                        complete_list.append(process_info(li_text))
                                    
                                    if len(complete_list) == 0:
                                        player_data += ["Undefined"]
                                    else:
                                        player_data += ["-".join(complete_list)]
                                        
                                except Exception:
                                    player_data += ["Undefined"]
                                
                                    
                            else:
                                player_data += ["Undefined"]*4
                                        
                        except Exception:
                            print('\n')
                            print("Problem reading data from: {}".format(processed))
                            print(str(e))
                            print('\n')
                            append_to_file("\nError reading data from: " + processed + "\n", logs_path)
                            append_to_file("Index: " + str(idx_1) + ", " + str(idx_2), logs_path)
                            append_to_file("Count: " + str(repeat_count), logs_path)
                            error = True
                                    
                        if error == False:
                            append_to_file(str({player: str(player_data)}), data)
                                    
                            print("\nSuccessfully retrieved from:\nTeam: " + str(idx_1) + "/" + str(teams_len) + "\nPlayer: " + str(idx_2) + "/" + str(players_len))
                            append_to_file("\nSuccessfully retrieved from:\nTeam: " + str(idx_1) + "/" + str(teams_len) + "\nPlayer: " + str(idx_2) + "/" + str(players_len), logs_path)
                            append_to_file("Count: " + str(repeat_count), logs_path)
                            
                        repeat_count -= 1
                        print("Count: " + str(repeat_count))
                        
                        if repeat == True and repeat_count == 0:
                            append_to_file("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++" + processed + "\n", logs_path)
                            append_to_file("\nCouldn't find any data in: " + processed + "\n", logs_path)
                            append_to_file("Index: " + str(idx_1) + ", " + str(idx_2), logs_path)
                            append_to_file("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++" + processed + "\n", logs_path)

            second_idx = 0
                
    sel.stop_server_and_driver(server, driver)
    return

def get_pending_players():
    pending = []
    not_pending = []
                            
    with open('players_data/players_data2.txt', 'r') as f:
        for line in f.readlines():
            line_dict = ast.literal_eval(line)
            key = line_dict.keys()[0]
            values = ast.literal_eval(line_dict.values()[0])
            
            count_undefined = 0
            for idx in range(len(values)):
                value = values[idx]
                if value == 'Undefined':
                    count_undefined += 1
            if 3 < count_undefined < 28:
                pending.append(str({"Tier":[key]}))
            elif 0 < count_undefined < 4 and values[-1] != 'Undefined' and values[-2] != 'Undefined' and \
            values[-3] != 'Undefined':
                pending.append(str({"Tier":[key]}))
            else:
                not_pending.append(line)
        
    with open('players_data/players_pending.txt', 'w') as f:
        for player in pending:
            f.write(player+"\n")
    with open('players_data/players_data_clean2.txt', 'w') as f:
        for player in not_pending:
            f.write(player+"\n")
        
def join_datasets():
    all_data = []
    with open('players_data/players_data_clean1.txt', 'r') as f:
        for line in f.readlines():
            all_data.append(line)
    with open('players_data/players_data_clean2.txt', 'r') as f:
        for line in f.readlines():
            all_data.append(line)
    with open('players_data/players_pending_data.txt', 'r') as f:
        for line in f.readlines():
            all_data.append(line)
    with open('players_data/players_pending_data2.txt', 'r') as f:
        for line in f.readlines():
            all_data.append(line)
            
    with open('players_data/players_all_data.txt', 'w') as f:
        for line in all_data:
            if line != '\n':
                f.write(line)
            
def to_csv():
    with open('players_data/whoscored_data.txt', 'r') as f:
        append_to_csv(FEATURES, 'players_data/whoscored_data.csv')
        for line in f.readlines():
            append_to_csv(ast.literal_eval(ast.literal_eval(line).values()[0]), 'players_data/whoscored_data.csv')
    
    
if __name__ == "__main__":
    #get_players_data(0, 0, 'players_data/players_pending.txt', 'players_data/players_pending_data.txt', 'players_data/players_pending_logs.txt')
    #get_pending_players()
    #join_datasets()
    to_csv()
    pass









