#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
=Selenium helper functions=
Use this functions to start and stop the Selenium server in every other module.
"""

from selenium import webdriver
import selenium.webdriver.chrome.service as service

"""
Path where the Selenium driver for your browser is saved.
Go to http://selenium-python.readthedocs.io/installation.html to search for the
appropiate driver, copy it to the directory where this script is saved,
and change 'chromedriver' to match the name of your driver.
"""
PATH_TO_DRIVER = './chromedriver'
"""
Path where your web browser application is saved. This example is for MacOs, in Windows 7, 8,
and 10, the path might be ‘C:\Program Files\Google\Chrome\Application’. Search Google if
you don't know how to find your browser application's path.
"""
PATH_TO_BROWSER = '/Applications/Google Chrome.app'
"""
Whoscored URL
"""
WHOSCORED_URL = 'https://www.whoscored.com'

"""
Functions
"""
def start_server_and_driver():
    """
    Start the Selenium server and driver and return them as objects.
    """
    
    server = service.Service(PATH_TO_DRIVER)
    server.start()

    capabilities = {'chrome.binary': PATH_TO_BROWSER}
    driver = webdriver.Remote(server.service_url, capabilities)
    
    return server, driver

def stop_server_and_driver(server, driver):
    """
    Close the driver and then stop the server.
    =Args=
        driver: driver object returned by def start_server_and_driver()
        server: server object returned by def start_server_and_driver()
    """
    
    driver.close()
    server.stop()
