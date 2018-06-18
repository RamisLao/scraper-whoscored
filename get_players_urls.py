#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
=Get Players' Urls=
Scrape all the teams' urls to find the urls of the players within them.
"""

import selenium_func as sel

import time
import bs4
import ast

from helper_functions import read_from_file, append_to_file, process_info


TEAMS_PATH = 'teams_urls/teams_urls.txt'
PLAYERS_PATH = 'players_urls/players_urls.txt'
LOGS_PATH = 'players_urls/players_logs.txt'

"""
Functions
"""  

def get_players_urls(teams_path, players_path, logs_path, first_idx, second_idx):
 
    server, driver = sel.start_server_and_driver()
    all_tier_teams = read_from_file(teams_path)
    
    all_tier_teams_length = len(all_tier_teams)-1
    
    for tier_teams in all_tier_teams[first_idx:]:
        
        tier_teams_dict = ast.literal_eval(tier_teams)
        teams = tier_teams_dict.values()[0]
        
        teams_len = len(teams)-1
        
        for team in teams[second_idx:]:
            repeat = True
            repeat_count = 10
            
            while repeat == True and repeat_count > 0:
            
                processed = process_info(team)
                error = False
                
                team_players = {}
                            
                try:
                    complete_url = sel.WHOSCORED_URL + team
                    
                    try:
                        driver.get(complete_url)
                        time.sleep(5)
                        
                        content = driver.page_source
                        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
                    except Exception as e:
                        print('\n')
                        print("Problem accessing {}".format(processed))
                        print(str(e))
                        print('\n')
                        append_to_file("\nError accessing: " + processed + "\n", logs_path)
                        append_to_file("Index: " + str(teams.index(team)) + ", " + str(all_tier_teams.index(tier_teams)), logs_path)
                        append_to_file("Count: " + str(repeat_count), logs_path)
                        continue
                    
                    table = soup.find("div", {"id": "statistics-table-" + 'summary' }).find("tbody", {"id": "player-table-statistics-body"})
        
                    hrefs = []
        
                    if table != None:
                        ahref = table.find_all('a', href=True)
                        
                        if ahref != None and len(ahref) > 0:
                    
                            for a in ahref:
                                href = a['href']
                                hrefs.append(process_info(href))
                            
                    if len(hrefs) > 0:
                        repeat = False
                    
                except Exception as e:
                    print('\n')
                    print("Problem reading data from: {}".format(processed))
                    print(str(e))
                    print('\n')
                    append_to_file("\nError reading data from: " + processed + "\n", logs_path)
                    append_to_file("Index: " + str(teams.index(team)) + ", " + str(all_tier_teams.index(tier_teams)), logs_path)
                    append_to_file("Count: " + str(repeat_count), logs_path)
                    error = True
                    
                if error == False:
                    team_players[processed] = hrefs
                    append_to_file(str(team_players), players_path)
                            
                    print("\nSuccessfully retrieved from:\nTier: " + str(all_tier_teams.index(tier_teams)) + "/" + str(all_tier_teams_length) + "\nTeams: " + str(teams.index(team)) + "/" + str(teams_len))
                    append_to_file("\nSuccessfully retrieved from:\nTier: " + str(all_tier_teams.index(tier_teams)) + "/" + str(all_tier_teams_length) + "\nTeams: " + str(teams.index(team)) + "/" + str(teams_len), logs_path)
                    append_to_file("Count: " + str(repeat_count), logs_path)
                        
                repeat_count -= 1
                print("Count: " + str(repeat_count))
                
                if repeat == True and repeat_count == 0:
                    append_to_file("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++" + processed + "\n", logs_path)
                    append_to_file("\nCouldn't find any data in: " + processed + "\n", logs_path)
                    append_to_file("Index: " + str(teams.index(team)) + ", " + str(all_tier_teams.index(tier_teams)), logs_path)
                    append_to_file("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++" + processed + "\n", logs_path)
            
        second_idx = 0
            
    sel.stop_server_and_driver(server, driver)
    return

        
if __name__ == "__main__":
    get_players_urls(0, 0)







