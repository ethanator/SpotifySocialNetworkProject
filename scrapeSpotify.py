#!/usr/bin/env python
# Scrape the Spotify Web Player and get the social network for a user.
#   Author: Yuxuan "Ethan" Chen
#     Date: November 7, 2014
#  Version: 0.9.1
#
# To-do:
#  - Add action to scroll down the page so that all artists or playlists can be loaded
#  - Better logic to wait for elements to load
#
# ===================================================
#                   VERSION HISTORY
# ===================================================
# Version 0.9.1 				  Posted Nov  7, 2014
#  - Can switch to the logged-in Spotify browse page
#  - Eliminate the unsupported command-line flag
#  - Can switch to the user profile page
#  - Can get iframes
#  - Can scrape user name
#  - Can click on the tabs on the user profile
#  - Can get recently played artists
#  - Can get public playlists
# ___________________________________________________
# Version 0.9                     Posted Nov  5, 2014
#  - Can log in Spotify
# ===================================================

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import getpass
import re
import sys
import time
import unicodedata

# Constants
SPOTIFY = 'http://play.spotify.com/'
SPOTIFY_USER = 'http://play.spotify.com/user'

# Open a broswer and navigate to the Spotify player
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"]) # Suppress a command-line flag
driver = webdriver.Chrome(chrome_options=options)					
driver.get(SPOTIFY)

# Click the "Already have an account" link
time.sleep(10)
login = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'has-account')))
login.click()

# Type in credentials at the command line to log in Spotiy with Facebook
print 'Spotify Social Network Project'
print '=============================='
time.sleep(10)
fb_login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'fb-login-btn')))
fb_login.click()
time.sleep(10)
driver.switch_to_window(driver.window_handles[1])
print 'Logging in via Facebook ...'
email_blank = driver.find_element_by_id('email')
pass_blank  = driver.find_element_by_id('pass')
input_email = raw_input('Email or Phone: ')
input_pass  = getpass.getpass('      Password: ')
email_blank.send_keys(input_email)
pass_blank.send_keys(input_pass)
email_blank.submit()

# Navigate from the browse page to the user page
print 'Waiting for Spotify to load ...'
time.sleep(10)
driver.switch_to_window(driver.window_handles[0])
driver.get(SPOTIFY_USER)
print 'Waiting for the user profile to load ...'
time.sleep(10)

# Locate the user iframe on the page
iframes = driver.find_elements_by_xpath("//iframe")
user_iframe = None
for iframe in iframes:
	if 'user-app-spotify' in iframe.get_attribute('id'):
		user_iframe = iframe
		break
driver.switch_to_default_content()
driver.switch_to.frame(user_iframe)

# Scrape the user name
print driver.find_element_by_xpath("//h1[@class='h-title']").text

# Scrape the recently played artists
recent_artists_tab = driver.find_element_by_xpath("//li[@data-navbar-item-id='recently-played-artists']")
recent_artists_tab.click()
print 'Waiting for the recently played artists list to load ...'
time.sleep(20)
recent_artists = driver.find_elements_by_xpath("//section[@class='recently-played-artists']/descendant::a[@class='mo-title']")
for artist in recent_artists:
	print artist.get_attribute('title')

# Scrape the public playlists
public_playlists_tab = driver.find_element_by_xpath("//li[@data-navbar-item-id='public-playlists']")
public_playlists_tab.click()
print 'Waiting for the public playlists to load ...'
time.sleep(20)
public_playlists = driver.find_elements_by_xpath("//section[@class='public-playlists']/descendant::a[@class='mo-title']")
for playlist in public_playlists:
	print playlist.get_attribute('title')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")