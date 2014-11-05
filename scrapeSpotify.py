#!/usr/bin/env python
# Scrape the Spotify Web Player and get the social network for a user.
#   Author: Yuxuan "Ethan" Chen
#     Date: November 5, 2014
#  Version: 0.9
# ===================================================
#                   VERSION HISTORY
# ===================================================
# Version 0.9                     Posted Nov  5, 2014
#  - 
# ===================================================

from bs4 import BeautifulSoup
import getpass
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import unicodedata

SPOTIFY = 'http://play.spotify.com/'
SPOTIFY_USER = 'http://play.spotify.com/user'

# Login to Spotify Web Player
driver = webdriver.Chrome()					
driver.get(SPOTIFY)
try:
  login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'has-account')))
  login.click()
  print 'Spotify Social Network Project'
  print '=============================='
  fb_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'fb-login-btn')))
  fb_login.click()
  driver.switch_to_window(driver.window_handles[1])
  print 'Logging in via Facebook ...'
  input_email = raw_input('Email or Phone: ')
  input_pass  = getpass.getpass('      Password: ')
  email_blank = driver.find_element_by_id('email')
  pass_blank  = driver.find_element_by_id('pass')
  email_blank.send_keys(input_email)
  pass_blank.send_keys(input_pass)
  email_blank.submit()
except:
  print 'Error!'
print 'Waiting for Spotify to load ...'
WebDriverWait(driver, 10)
driver.get(SPOTIFY_USER)