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

class CaseConverter():
    def run(self):

        locations = Locations()

        with open('data/original/cases_confirmed_full.csv', encoding='utf-16') as csvfile:
            source_rows = csv.DictReader(csvfile, delimiter='\t')

            timezone = pytz.timezone("Europe/Zurich")

            target_rows = []
            for source_row in source_rows:
            #for source_row in source_rows:
                target_row = {}

                # All original fields are listed below in unchanged order. Skipped fields are maked with pass statement (noop)

                # Geschlecht
                gender = source_row['Geschlecht'].lower()
                gender = gender.replace("männlich","male")
                gender = gender.replace("weiblich","female")
                target_row['gender'] = gender

                # Tooltip_incidence_de
                pass

                # Altersklasse
                pass

                # Datum
                #date = timezone.localize(dateutil.parser.parse(source_row['Datum']))
                if source_row['Datum'] != "":
                    date = datetime.strptime(source_row['Datum'], '%d.%m.%Y')
                    target_row['date'] = date.isoformat(sep='T', timespec='auto')
                else:
                    target_row['date'] = None

                # Kanton
                target_row['canton_abbr'] = source_row['Kanton']
                
                # ktn
                pass

                # akl
                target_row['age_class'] = source_row['akl'].replace(' ', '')

                # Canton
                pass

                # Classe d'âge
                pass

                # Date
                pass

                # Excluded_for_incomplete_data
                pass

                # fall_dt Date of confirmed infected
                #if source_row['fall_dt'] != "":
                #    case_date = timezone.localize(dateutil.parser.parse(source_row['fall_dt']))
                #    target_row['case_date'] = case_date.isoformat(sep='T', timespec='auto')
                #else:
                #    target_row['case_date'] = None
                pass

                # pttoddat
                #if source_row['pttoddat'] != "":
                #    death_date = timezone.localize(dateutil.parser.parse(source_row['pttoddat']))
                #    target_row['death_date'] = death_date.isoformat(sep='T', timespec='auto')
                #else:
                #    target_row['death_date'] = None
                pass

                # replikation_dt
                #replication_timestamp = timezone.localize(dateutil.parser.parse(source_row['replikation_dt']))
                # Date format changed!
                replication_timestamp = timezone.localize(datetime.strptime(source_row['replikation_dt'], '%d/%m/%Y %H:%M:%S'))
                target_row['last_update'] = replication_timestamp.isoformat(sep='T', timespec='auto')

                if target_row['date'] == None:
                    target_row['date'] == target_row['last_update']
                
                # replikation_dt (copy)
                pass

                # Sexe
                pass

                # Switch_Bilan_de
                pass

                # Switch_Bilan_fr
                pass

                # titre_dashboard2_d
                pass
                
                # titre_dashboard2_f
                pass

                # Tooltip_incidence_fr
                pass

                # Anzahl laborbestätigte Fälle
                target_row['infected'] = int(source_row['Anzahl laborbestätigte Fälle'])
                
                # Anzahl Todesfälle
                target_row['death'] = int(source_row['Anzahl Todesfälle'])

                # Cas confirmés en laboratoire
                pass

                # Cas décédés excluded
                pass

                # F1
                target_row['f1'] = int(source_row['F1'])

                # fallklasse_3
                target_row['case_class_3'] = int(source_row['fallklasse_3'])

                # Laborbestätigte Fälle excluded
                pass

                # Nombre de cas confirmés en laboratoire
                pass

                # Nombre de cas décédés
                pass

                # Number of Records (Not available anymore)
                #target_row['number_of_records'] = int(source_row['Number of Records'])

                # pttod_1
                pass

                # sex
                pass

                # Todesfälle_excluded
                pass

                ## Additional fields
                # Country abbreviation
                target_row['country_abbr'] = "CH"

                # Country latitude
                target_row['country_lat'] = locations.get("CH").latitude

                # Country longitude
                target_row['country_long'] = locations.get("CH").longitude

                # Canton latitude
                target_row['canton_lat'] = locations.get(target_row['canton_abbr']).latitude

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
            target_rows.sort(key=lambda k:  k['f1'])

        # Store file
        filename = 'cases_confirmed_full.csv' 

        with open(os.path.join('./data/converted/', filename), 'w+', newline='', encoding='utf-8') as target_file:
            fieldnames = ['last_update', 'date', 'country_abbr', 'canton_abbr', 'age_class', 'gender', 'infected', 'death', 'f1', 'case_class_3', 'number_of_records', 'country_lat', 'country_long', 'canton_lat', 'canton_long', 'country_en', 'canton_en', 'country_de', 'canton_de']
            writer = csv.DictWriter(target_file, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in target_rows:
                writer.writerow(row)
