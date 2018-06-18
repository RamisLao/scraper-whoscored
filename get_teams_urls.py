#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
=Get teams' urls=
Scrape TIERS_URLS to find all the urls of the teams that are within those tiers.
"""
import time
import bs4

import selenium_func as sel
from helper_functions import read_from_file, append_to_file


TIERS_PATH = 'tiers_urls/tiers_urls.txt'
TEAMS_PATH = 'teams_urls/teams_urls.txt'
TEAMS_LOGS = 'teams_urls/teams_logs.txt'

"""
Functions
"""

def get_teams_urls(start_idx):
    """
    Searches each tier and extracts all the teams' urls within that tier.
    """
    server, driver = sel.start_server_and_driver()
    tiers_urls = read_from_file(TIERS_PATH)

    length = len(tiers_urls)
    
    for tier in tiers_urls[start_idx:]:
        error = False
        teams_urls = []
        
        try:
            complete_url = sel.WHOSCORED_URL + tier
        
            try:
                driver.get(complete_url)
                        
                content = driver.page_source
                soup = bs4.BeautifulSoup(''.join(content), 'lxml')
            except Exception as e:
                print('\n')
                print("Problem accessing {}".format(tier))
                print(str(e))
                print('\n')
                append_to_file("\nError accessing: " + tier + "\n", TEAMS_LOGS)
                append_to_file("Index: " + str(tiers_urls.index(tier)), TEAMS_LOGS)
                continue
            
            stage = None
            stages_div = soup.find('div', {'id':'sub-navigation'})
            if stages_div != None:
                stage_li = stages_div.find_all('li')[0]
                if stage_li != None:
                    stage_href = stage_li.find('a', href=True)['href']
                    if stage_href != None:
                        stage = stage_href.split('/')[8]
                
            if stage != None:
                standings_table = soup.find('div', {'id':'standings-'+stage})
                standings_tbody = standings_table.find(id='standings-'+stage+'-content')
                teams_tr = standings_tbody.find_all('tr')
                                
                if len(teams_tr) > 0:
                    for tr in teams_tr:
                        team_td = tr.find_all('td')[1]
                        team_href = team_td.find('a', href=True)['href']
                        teams_urls.append(team_href)
                        
        except Exception as e:
            print('\n')
            print("Problem reading data from: {}".format(tier))
            print(str(e))
            print('\n')
            append_to_file("\nError reading data from: " + tier + "\n", TEAMS_LOGS)
            append_to_file("Index: " + str(tiers_urls.index(tier)), TEAMS_LOGS)
            error = True
            
        if error == False:
            if len(teams_urls) > 0:
                to_store = {tier:teams_urls}
                append_to_file(str(to_store), TEAMS_PATH)
                    
            append_to_file("\nSuccessfully retrieved from: " + str(tiers_urls.index(tier)) + "/" + str(length), TEAMS_LOGS)
                
        time.sleep(1)
        
    sel.stop_server_and_driver(server, driver)
    return
        

if __name__ == '__main__':
    get_teams_urls(0)





