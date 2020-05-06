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
import time
import json
import logging
import git 

# TODO: Improve logging
# TODO: Improve comments

### Git Repository
class Pusher():
  def setup(self, git_dir):
    # Load Repo 
    self.repo = git.Repo(git_dir)
    # Get current state
    self.current = self.repo.head.commit
    self.repo.remotes.origin.pull()
    if self.current == self.repo.head.commit:
      logging.info("Git Pusher setup: Git Repository up to date")
    else:
      logging.info("Git Pusher setup: Git Repository updated")
  
  def run(self):
    git = self.repo.git
    git.add('Sheet_4_(d)_Full_Data_data.csv')
    git.add('foph_covid19_data_converted_unix.csv')
    git.add('last_updated.txt')
    commit_message = "Data updated: "
    self.repo.index.commit(commit_message)
    git.push()

