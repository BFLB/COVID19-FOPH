#!/usr/bin/env python3

#####################################################################################################################
# 
# Copyright (c) 2020 Bernhard Flühmann. All rights reserved.
#
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.
#
######################################################################################################################

# This script creates standardized, translated versions of the covid-19 case file downloaded from the website of
# FOPH (BAG) of switzerland. https://covid-19-schweiz.bagapps.ch/de-1.html
#

# TODO: Improve logging
# TODO: Add coordinates
# TODO: Add Switzerland
# TODO: Add canton names
# TODO: Improve comments

import os
import csv
from datetime import datetime
import pytz
import sys
import dateutil.parser
import logging
from templates import Locations
import openpyxl
from openpyxl import Workbook
from pandas import read_excel

class CaseConverter():
    def run(self):

        locations = Locations()

        timezone = pytz.timezone("Europe/Zurich")

        target_rows = []

        my_sheet = 'Dashboard_1_2' # change it to your sheet name
        file_name = 'data/original/cases_confirmed_full.xlsx' # change it to the name of your excel file
        df = read_excel(file_name, sheet_name = my_sheet)
        #df.fillna("")
        #print(df.head()) # shows headers with top 5 rows

        # for row in df.itertuples():
        #     print(row)

        for row in df.itertuples():
            target_row = {}

            # replikation_dt
            #replication_timestamp = timezone.localize(dateutil.parser.parse(source_row['replikation_dt']))
            #replication_dt = row[1]
            #replication_timestamp = timezone.localize(datetime.strptime(row[1].date_string, '%y.%m.%d %H:%M:%S'))
            replication_timestamp = row[1]
            target_row['last_update'] = replication_timestamp.isoformat(sep='T')

            # fall_dt and pttoddat are mutually exclusive. Nevertheless rows may contain both infected and deaths!
            # Sometimes the date is missing. In this cases we set it to the replication_dt
            target_row['date'] = replication_timestamp.isoformat(sep='T')
            
            # fall_dt
            fall_dt = row[2]
            if isinstance(fall_dt, str): # Workaround for stupid nan value
                if fall_dt != "":
                    timestamp = timezone.localize(datetime.strptime(fall_dt, '%Y-%m-%d'))
                    target_row['date'] = timestamp.isoformat(sep='T', timespec='auto')
 
            # ktn
            target_row['canton_abbr'] = row[3]

            # akl
            target_row['age_class'] = row[4].replace(' ', '')


            # sex
            gender_code = row[5]
            if gender_code == 1:
                target_row['gender'] = "male"
            else:
                target_row['gender'] = "female"
                
            # Geschlecht
            pass
            
            
            # Sexe
            pass


            # fallklasse 3
            #target_row['case_class_3'] = int(row[8]) # Deprecated
            target_row['infected']     = int(row[8])


            # pttoddat
            pttoddat = row[9]
            if isinstance(pttoddat, str): # Workaround for stupid nan value
                if fall_dt != "":
                    timestamp = timezone.localize(datetime.strptime(pttoddat, '%Y-%m-%d'))
                    target_row['date'] = timestamp.isoformat(sep='T', timespec='auto')


            # pttod
            target_row['death'] = int(row[10])


            ## Additional fields
            # Country abbreviation
            target_row['country_abbr'] = "CH"

            # Country latitude
            target_row['country_lat'] = locations.get("CH").latitude

            # Country longitude
            target_row['country_long'] = locations.get("CH").longitude

            # Canton latitude
            #try:
            target_row['canton_lat'] = locations.get(target_row['canton_abbr']).latitude
            #except: # catch *all* exceptions
            #    print(row)
            # Canton longitude
            target_row['canton_long'] = locations.get(target_row['canton_abbr']).longitude

            # Country name english
            target_row['country_en'] = locations.get("CH").name_en

            # Canton name english 
            target_row['canton_en'] = locations.get(target_row['canton_abbr']).name_en

            # Country name german
            target_row['country_de'] = locations.get("CH").name_de

            # Canton name german 
            target_row['canton_de'] = locations.get(target_row['canton_abbr']).name_de

            # Add row to rows
            target_rows.append(target_row)

            # Sort rows
            #target_rows.sort(key=lambda k:  k['f1'])

        # Store file
        filename = 'cases_confirmed_full_new.csv' 

        with open(os.path.join('./data/converted/', filename), 'w+', newline='', encoding='utf-8') as target_file:
            fieldnames = ['last_update', 'date', 'country_abbr', 'canton_abbr', 'age_class', 'gender', 'infected', 'death', 'country_lat', 'country_long', 'canton_lat', 'canton_long', 'country_en', 'canton_en', 'country_de', 'canton_de']
            writer = csv.DictWriter(target_file, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in target_rows:
                writer.writerow(row)
