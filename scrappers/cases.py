#!/usr/bin/env python3

#####################################################################################################################
# 
# Copyright (c) 2020 Bernhard Flühmann. All rights reserved.
#
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.
#
######################################################################################################################


import time
import json
import logging
import test
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import chromedriver_binary # Install binary: pip install chromedriver-binary

# TODO: Improve logging
# TODO: Improve comments

### Selenium scrapper class
class CaseScrapper():
  def setup(self, headless):
    self.options = Options()
    if headless == True:
      self.options.add_argument("--headless")
    self.driver = webdriver.Chrome(options=self.options)
    self.vars = {}
  
  def teardown(self):
    self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def run(self, replication_date):
    self.driver.get("https://covid-19-schweiz.bagapps.ch/de-1.html")
    self.driver.set_window_size(1920, 1080)
    self.driver.switch_to.frame(0)
    time.sleep(5)
    curr_date = self.driver.find_element(By.CSS_SELECTOR, "#title8489910619019530759_8666137308565905127 .tab-textRegion-content div:nth-child(1) > span").text.replace("Bilanz am ","")
    #curr_date = self.driver.find_element(By.CSS_SELECTOR, "#title8489910619019530759_8666137308565905127 span:nth-child(2)").text

    # Check if data from today #
    if replication_date != None:
      search_date = "{:02}.{:02}.{}".format(replication_date.day, replication_date.month, replication_date.year)
      if curr_date != search_date:
        error_message = "Scraping skipped: Replication date of website data is {}. must be {}".format(curr_date, search_date)
        logging.info(error_message)
        self.driver.close()
        return True
        
    # Select and unselect male. Needed to activate the data download button.
    self.driver.implicitly_wait(3)
    self.driver.find_element(By.CSS_SELECTOR, "#view8489910619019530759_1658786962355642485 .tabCanvas:nth-child(2)").click()
    time.sleep(10)
    self.driver.find_element(By.CSS_SELECTOR, "#view8489910619019530759_1658786962355642485 .tabCanvas:nth-child(2)").click()
    # Click download
    #self.driver.implicitly_wait(10)
    time.sleep(10)
    self.driver.find_element(By.CSS_SELECTOR, ".tab-icon-download").click()
    self.vars["window_handles"] = self.driver.window_handles
    # Click daten
    time.sleep(10)
    self.driver.find_element(By.CSS_SELECTOR, ".fppw03o:nth-child(3)").click()
    self.vars["win3856"] = self.wait_for_window(2000)
    self.vars["root"] = self.driver.current_window_handle
    self.driver.switch_to.window(self.vars["win3856"])
    # Click Vollständige Daten (all data)
    time.sleep(5)
    self.driver.find_element(By.XPATH, "//li[contains(.,\'Full Data\')]").click()
    # Click Alle Spalten anzeigen (all columns)
    time.sleep(10)
    self.driver.find_element(By.CSS_SELECTOR, ".f81g0pf").click()
    time.sleep(5)
    self.vars["window_handles"] = self.driver.window_handles
    time.sleep(10)
    self.driver.find_element(By.CSS_SELECTOR, ".tab-top-info .csvLink").click()
    #self.driver.find_element(By.LINK_TEXT, "Alle Zeilen als Textdatei herunterladen").click()
    self.vars["win5720"] = self.wait_for_window(2000)
    #self.driver.switch_to.window(self.vars["win5720"])
    #self.driver.implicitly_wait(10)
    time.sleep(40)
    self.driver.close()
    self.driver.switch_to.window(self.vars["root"])

    # Move file
    src = "Sheet_4_(d)_Full_Data_data.csv"
    dst = "data/original/cases_confirmed_full.csv"
    shutil.move(src,dst)


    return False