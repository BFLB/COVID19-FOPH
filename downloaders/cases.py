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
import urllib

class CaseScrapper():
  def run(self):
    self.outfile = "data/original/cases_confirmed_full.xlsx"
    self.url = "http://www.muellerindustries.com/uploads/pdf/UW%20SPD0114.xls"
    urllib.request.urlretrieve(self.url, self.outfile) 
