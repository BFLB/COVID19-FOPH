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

import csv
from datetime import datetime
import pytz
import sys
import dateutil.parser
import logging
from templates import Locations

class Converter():
    def convert(self):

        locations = Locations()

        with open('Sheet_4_(d)_data.csv', encoding='utf-16') as csvfile:
            source_rows = csv.DictReader(csvfile, delimiter='\t')

            timezone = pytz.timezone("Europe/Zurich")

            target_rows = []
            for index, source_row in enumerate(source_rows):
            #for source_row in source_rows:
                target_row = {}

                # All original fields are listed below in unchanged order. Skipped fields are maked with pass statement (noop)

                # Classe d'âge
                pass

                # Canton
                canton = source_row['Canton']
                target_row['canton_abbr'] = canton

                # Todesfälle_excluded
                pass

                # Excluded_for_incomplete_data
                pass

                # titre_dashboard2_f
                pass

                # Tooltip_incidence_de
                pass

               # Anzahl Todesfälle
                pass

                # Switch_Bilan_de
                pass

                # Nombre de cas confirmés en laboratoire
                pass

                # Nombre de cas décédés
                pass

                # Date_Décédé_CasConfirmés
                pass # TODO: cross-check with falldatum

                # Kanton
                pass

                # Cas décédés excluded
                pass

                # Altersklasse
                pass

                # Datum_Todes_LaborsFälle TODO: cross-check with falldatum, ambiguous field name
                # Datum_Todes_LaborsFälle TODO: cross-check with falldatum, ambiguous field name
                #confirmed_date = timezone.localize(dateutil.parser.parse(source_row['Datum_Todes_LaborsFälle']))
                confirmed_date = timezone.localize(datetime.strptime(source_row['Datum_Todes_LaborsFälle'], '%d.%m.%Y'))
                target_row['confirmed_date'] = confirmed_date.isoformat(sep='T', timespec='auto')

                # F1
                target_row['case_number'] = int(source_row['F1'])

                # Geschlecht
                gender = source_row['Geschlecht']
                gender = gender.replace("männlich","male")
                gender = gender.replace("weiblich","female")
                target_row['gender'] = gender

                # Anzahl der Datensätze
                pass # TODO: Error if not 1

                # Sexe
                pass

                # Switch_Bilan_fr
                pass

                # Tooltip_incidence_fr
                pass

                # akl
                target_row['age_class'] = source_row['akl'].replace(' ', '')

                # altersjahr
                target_row['age'] = source_row['altersjahr']

                # fall_dt
                case_date = timezone.localize(dateutil.parser.parse(source_row['fall_dt']))
                target_row['case_date'] = case_date.isoformat(sep='T', timespec='auto')

                # fallklasse
                case_class = source_row['fallklasse']
                case_class = case_class.replace("sicherer Fall","confirmed")
                target_row['case_class'] = case_class

                # ktn
                pass

                # Anzahl laborbestätigte Fälle
                target_row['confirmed'] = bool(source_row['Anzahl laborbestätigte Fälle'])

                # pttod
                death = source_row['pttod']
                if death == "1":
                    target_row['death'] = True
                else:
                    target_row['death'] = None
 
                # pttoddat
                if source_row['pttoddat'] != "":
                    death_date = timezone.localize(dateutil.parser.parse(source_row['pttoddat']))
                    target_row['death_date'] = death_date.isoformat(sep='T', timespec='auto')
                else:
                    target_row['death_date'] = None

                # replikation_dt (copy)
                pass

                # replikation_dt
                replication_timestamp = timezone.localize(dateutil.parser.parse(source_row['replikation_dt']))
                target_row['replication_date'] = replication_timestamp.isoformat(sep='T', timespec='auto')

                # sex
                pass

                # titre_dashboard2_d
                pass

                ### Additional columns

                # Country abbreviation
                target_row['country_abbr'] = "CH"

                # Country latitude
                target_row['country_lat'] = locations.get("CH").latitude

                # Country longitude
                target_row['country_long'] = locations.get("CH").longitude

                # Canton latitude
                target_row['canton_lat'] = locations.get(canton).latitude

                # Canton longitude
                target_row['canton_long'] = locations.get(canton).longitude

                # Country name english
                target_row['country_name_en'] = locations.get("CH").name_en

                # Canton name english 
                target_row['canton_name_en'] = locations.get(canton).name_en

                # Country name german
                target_row['country_name_de'] = locations.get("CH").name_de

                # Canton name german 
                target_row['canton_name_de'] = locations.get(canton).name_de




                # Some cases are marked as death but death date is missing. Set death_date_missing and the death date to replication date.
                # This is not correct but the best we can do.
                if target_row['death'] == True and target_row['death_date'] == None:
                    target_row['death_date_missing'] = True
                    target_row['death_date'] == target_row['replication_date']

                # Add row to rows
                target_rows.append(target_row)

                ## Checks
                if case_date != confirmed_date:
                    logmessage = "Line {}: case_date {} does not match confirmed_date {}".format(index + 1, case_date.isoformat(sep='T', timespec='auto'), confirmed_date.isoformat(sep='T', timespec='auto'))
                    logging.info(logmessage)

        # Sort rows
        target_rows.sort(key=lambda k:  k['case_number'])

        with open('FOPH_Covid19_full_converted_unix.csv', 'w+', newline='', encoding='utf-8') as target_file:
            fieldnames = ['case_number', 'case_class', 'case_date', 'canton_abbr', 'gender', 'age_class', 'age', 'confirmed', 'confirmed_date', 'death', 'death_date', 'death_date_missing', 'replication_date', 'country_abbr', 'country_lat', 'country_long', 'canton_lat', 'canton_long', 'country_name_en', 'canton_name_en', 'country_name_de', 'canton_name_de']
            writer = csv.DictWriter(target_file, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for row in target_rows:
                writer.writerow(row)
