#!/usr/bin/env python3

#####################################################################################################################
# 
# Copyright (c) 2020 Bernhard Flühmann. All rights reserved.
#
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.
#
######################################################################################################################

from datetime import date
from datetime import datetime
import sys
import time
import json
import os
import logging
import argparse
import pytz
from data_scraper import Scraper
from data_converter import Converter 
from data_pusher import Pusher



# TODO: Improve logging
# TODO: Improve comments
# TODO: Add more options
# TODO: Add git push
# TODO: Test

### Command line arguments
parser = argparse.ArgumentParser(description='Scrape FOPH covid-19 case file from https://covid-19-schweiz.bagapps.ch/de-1.html')
parser.add_argument("--loglevel", type=str, dest="loglevel", default="WARNING", help='log level')
parser.add_argument("--logdest", type=str, dest="logdest", default="stdout", help='log file. Defaults to stdout')
parser.add_argument("--target", type=str, default="./data/tableau/original/foph-covid19-tableau-cases-full-original.csv", help='Target file')
parser.add_argument('--scrap', dest='scrap', action='store_true', help='Scrap data')
parser.add_argument('--convert', dest='convert', action='store_true', help='Create converted data file')
parser.add_argument('--push', dest='push', action='store_true', help='Push data to GitHub')
parser.add_argument('--not-headless', dest='headless', action='store_false', help='Disable headless mode')
parser.add_argument('--ignore-date', dest='ignore_date', action='store_true', help='Ignore replication date of data on website')
parser.set_defaults(srcap=False, convert=False, push=False, headless=True, ignore_date=False)
args = parser.parse_args()

### Init
# Set timezone  
timezone = pytz.timezone("Europe/Zurich")


### Logging setup
numeric_level = getattr(logging, args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % args.loglevel)

if args.logdest.lower() == "stdout":
  logging.basicConfig(level=numeric_level)
else:
  logging.basicConfig(level= numeric_level, filename= args.logdest)

logging.debug("logging.level= " + args.loglevel + ", logging.filename=" + args.logdest)


# Git Setup
if args.push == True:
  pusher = Pusher()
  pusher.setup('./')


# Date preparation
skip = False
today = None

if args.ignore_date == False:
  today = date.today()
  try:
    with open("last_updated.txt", encoding='utf-8') as last_updated:
      replication_date = timezone.localize(datetime.fromisoformat(last_updated.read())).date()

    # Compare with today
    if today.isoformat() == replication_date.isoformat():
    #if today.day == replication_date.day and today.month == replication_date.month and today.year == replication_date.year:
      logging.info("Files are already up to date. Done")
      exit()

  except (OSError, IOError, FileNotFoundError) as e:
    logging.debug(e)
    pass

  except Exception:
    exit()

#### Run scraper
if args.scrap == True:
  logging.info('Start scrapping')
  scraper = Scraper()
  scraper.setup(args.headless)
  skipped = scraper.run(today)
  scraper.teardown()
  logging.info('Scrapping finished')

  if skipped == True:
    exit()
else:
  logging.info("Scraping disabled, skipped. Use --scrape to enable")

### Convert file
if args.convert == True:
  logging.info('Start converting')
  converter = Converter()
  converter.run()

  # Update last_updated
  with open("last_updated.txt", 'w+', newline='') as last_updated:
    if today == None:
      today = date.today()
    today_str = today.isoformat()
    last_updated.write(today_str)
  logging.info('Converting finished')
else:
  logging.info("Converting disabled, skipped. Use --convert to enable")

### Push data to GitHub
if args.push == True:
  logging.info("Start pushing")
  pusher.run()
  logging.info("Pushing finished")
else:
  logging.info("Pushing disabled, skipped. Use --push to enable")
