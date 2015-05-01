#!/usr/bin/env python
# Scrape the Spotify Web Player and get the social network for a user.
#   Authors: Yuxuan "Ethan" Chen, Garrett McGrath
#     Date: April 30, 2014
#  Version: 0.9.5
#
# To-do:
#  - Clean code according to Google Python style guide
#
# ===================================================
#                   VERSION HISTORY
# ===================================================
# Version 0.9.5                   Posted Apr 30, 2014
#
# ___________________________________________________
# Version 0.9.4                   Posted Nov 13, 2014
#  - Removed time.sleep(10) calls, explicit waits now
#  - Changed scraping to class SpotifyScrape in
#    anticipation of logging and database storage
#  - Simplified iframe transitions
#  - Created continuous queue of profile scrapes
#  - Can support users with no recent artists
#  - Can support users with no public playlists
#  - Scrapes users followings as well as followers
#  - Can support users without followings
#  - Improved scrolling capability
#  - Created the wrapper function 'gather' which
#    automatically scrolls down and scrapes all
#    elements in playlists, followers, and following
#  - Enabled MySQL database storage of results
# ___________________________________________________
# Version 0.9.3 		  Posted Nov 10, 2014
#  - Can scrape the followers.
#  - Can load all the playlists and scrape them.
# ___________________________________________________
# Version 0.9.2      		  Posted Nov  8, 2014
#  - Can scroll to the bottom
# ___________________________________________________
# Version 0.9.1 		  Posted Nov  7, 2014
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import getpass
import string

class SpotifyScraper:
    def __init__(self):
        self.q = []
        self.q.append('spotify')
        self.driver = None
        #self.db = MySQLdb.connect("localhost", "ubuntu", "", "spotify")

    def connect(self):
        print 'Spotify Social Network Project'
        print '=============================='

        # Open a broswer and navigate to the Spotify player
        print 'Creating webdriver ...'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", 
		["ignore-certificate-errors"]) # Suppress a command-line flag
        self.driver = webdriver.Chrome(chrome_options=options, 
		service_args=["--verbose", "--log-path=webdriver.log"])
        self.driver.implicitly_wait(2)

        print 'Navigating to Spotify ...'
        self.driver.get('http://play.spotify.com/')

        # Click the "Already have an account" link
        login = WebDriverWait(self.driver, 10).until(
		EC.element_to_be_clickable((By.ID, 'has-account')))
        login.click()

        # Type in credentials at the command line to log in Spotiy with Facebook
        fb_login = WebDriverWait(self.driver, 10).until(
		EC.element_to_be_clickable((By.ID, 'fb-login-btn')))
        fb_login.click()
        self.driver.switch_to_window(self.driver.window_handles[1])
        print 'Logging in via Facebook ...'
        email_blank = self.driver.find_element_by_id('email')
        pass_blank  = self.driver.find_element_by_id('pass')
        input_email = raw_input('Email or Phone: ')
        input_pass  = getpass.getpass('      Password: ')
        email_blank.send_keys(input_email)
        pass_blank.send_keys(input_pass)
        email_blank.submit()

        # Navigate from the browse page to the user page
        print 'Waiting for Spotify to load ...'
        self.driver.switch_to_window(self.driver.window_handles[0])
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='item-profile etched-top has-extra-bottom-row show show show show']")))
        print 'Connection complete ...'
        print '=============================='

    def scrape(self):
        # Load user page
        user = self.q.pop(0)
        print 'Scraping user: ' + user
        self.driver.get('http://play.spotify.com/user/' + user)
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@id, 'user')]")))
        # Scrape user name
        print 'Scraping user name ...'
        WebDriverWait(self.driver, 20).until(lambda x: self.driver.find_element_by_xpath("//h1[@class='h-title']").text)
        name = self.driver.find_element_by_xpath("//h1[@class='h-title']").text
        print name
        # Scrape recently played artists
        artists = self.gather('recently-played-artists')
        for artist in artists:
            self.store('recent_artists', ['id', 'user'], [artist, user])
        # Scrape public playlists
        playlists = self.gather('public-playlists')
        for playlist in playlists:
            self.store('playlists', ['id', 'user'], [playlist, user])
        # Scrape following
        following = self.gather('following')
        for follow in following:
            self.store('follows', ['outgoing', 'incoming'], [user, follow])
            self.q.append(follow)
        # Scrape followers
        followers = self.gather('followers')
        for follower in followers:
            self.store('follows', ['outgoing', 'incoming'], [follower, user])
            self.q.append(follower)
        #self.db.commit()

    def gather(self, type):
        try:
            print 'Scraping ' + type + ' ...'
            tab = self.driver.find_element_by_xpath("//li[@data-navbar-item-id='" + type + "']")
            tab.click()
            if len(self.driver.find_elements_by_xpath("//section[@class='" + type + "']/descendant::a[contains(@class, 'title')]")) > 20:
                while True:
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    try:
                        WebDriverWait(self.driver, 2).until(lambda x: self.driver.execute_script('return document.body.scrollHeight != document.body.scrollTop + window.innerHeight;'))
                    except:
                        break
            self.driver.execute_script('window.scrollTo(0, 0);')
            items = self.driver.find_elements_by_xpath("//section[@class='" + type + "']/descendant::a[contains(@class, 'title')]")
            for i in xrange(len(items)):
                items[i] = items[i].get_attribute('href').split('/')[-1]
            return items
        except NoSuchElementException:
            print 'No ' + type
            return []

    def store(self, table, fields, values):
        print values
        #cur = self.db.cursor()
        #cur.execute('INSERT INTO ' + table + "(" + string.join(fields, ", ") + ") VALUES ('" + string.join(values, "', '") + "');")
        #cur.close()

    def close(self):
        self.driver.close()
        self.db.close()

if __name__ == '__main__':
    scraper = SpotifyScraper()
    scraper.connect()
    while scraper.q:
        scraper.scrape()
    scraper.close()
