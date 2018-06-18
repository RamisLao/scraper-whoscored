#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
=Get teams' urls=
Scrape TIERS_URLS to find all the urls of the teams that are within those tiers.
"""
import time
import bs4

import selenium_func as sel
from helper_functions import save_to_file

"""
Path to store the complete list of teams' urls
"""
TIERS_PATH = 'tiers_urls/tiers_urls.txt'


"""
Functions
"""

def get_tiers_urls():
    """
    Searches each tier and extracts all the tiers' urls available.
    """
    
    server, driver = sel.start_server_and_driver()
        
    tiers_urls = []
    try:    
        driver.get(sel.WHOSCORED_URL)
        
        time.sleep(10) #Go to the browser, click All Leagues & Cups and then select All
        
        content = driver.page_source
        soup = bs4.BeautifulSoup(''.join(content), 'lxml')
        
        regions = soup.find("div", {"id": "domestic-regions"})
        li = regions.find_all("li")
        
        for l in li:
            ul = l.find("ul")
            if ul is None:
                continue
            sub_li = ul.find_all("li")
            
            for sub in sub_li:
                href = sub.find('a', href=True)['href']
                tiers_urls.append(href)
        
    except Exception as e:
        print("Error")
        print(str(e))
        
    save_to_file(tiers_urls, TIERS_PATH)
    sel.stop_server_and_driver(server, driver)
    
    return
    

if __name__ == '__main__':
    get_tiers_urls()





