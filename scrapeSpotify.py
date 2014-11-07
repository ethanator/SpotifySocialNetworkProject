#!/usr/bin/env python
# Scrape the Spotify Web Player and get the social network for a user.
#   Author: Yuxuan "Ethan" Chen
#     Date: November 7, 2014
#  Version: 0.9.1
# ===================================================
#                   VERSION HISTORY
# ===================================================
# Version 0.9.1 				  Posted Nov  7, 2014
#  - Can switch to the logged-in Spotify browse page
#  - Eliminate the unsupported command-line flag
#  - Can switch to the user profile page
#  - Can get iframes
# ___________________________________________________
# Version 0.9                     Posted Nov  5, 2014
#  - Can log in Spotify
# ===================================================

from bs4 import BeautifulSoup
import getpass
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
import unicodedata

SPOTIFY = 'http://play.spotify.com/'
SPOTIFY_USER = 'http://play.spotify.com/user'

# Login to Spotify Web Player
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
driver = webdriver.Chrome(chrome_options=options)					
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
time.sleep(10)
driver.switch_to_window(driver.window_handles[0])
driver.get(SPOTIFY_USER)
print 'Waiting for the user profile to load ...'
time.sleep(10)
soup = BeautifulSoup(driver.page_source)
print soup.findAll('iframe', id=re.compile('^user'))