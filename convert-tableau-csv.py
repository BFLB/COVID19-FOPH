#!/usr/bin/env python3

#####################################################################################################################
# 
# Copyright (c) 2016 Thomas Owens. All rights reserved.
#
# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.
#
######################################################################################################################

# This script creates standardized, translated versions of the covid-19 case file downloaded from the website of
# FOPH (BAG) of switzerland. https://covid-19-schweiz.bagapps.ch/de-1.html
#


import csv
from datetime import datetime
import pytz
import sys
import argparse

parser = argparse.ArgumentParser(description='Convert FOPH covid-19 case files to standardized english versions.')
parser.add_argument('source', type=str, help='Source file')
parser.add_argument('target', type=str, help='Target file')

args = parser.parse_args()

with open(args.source, encoding='utf-16') as csvfile:
    source_rows = csv.DictReader(csvfile, delimiter='\t')

    timezone = pytz.timezone("Europe/Zurich")

    target_rows = []

    for source_row in source_rows:
        target_row = {}

        # All original fields are listed below in unchanged order. Skipped fields are maked with pass statement (noop)

        # Classe d'âge
        pass

        # Canton
        target_row['canton_abbr'] = source_row['Canton']

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
        confirmed_date = timezone.localize(datetime.strptime(source_row['fall_dt'], '%d.%m.%Y'))
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
        case_date = timezone.localize(datetime.strptime(source_row['fall_dt'], '%d.%m.%Y'))
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
            death_date = timezone.localize(datetime.strptime(source_row['pttoddat'], '%d.%m.%Y'))
            target_row['death_date'] = replication_timestamp.isoformat(sep='T', timespec='auto')
        else:
            target_row['death_date'] = None

        # replikation_dt (copy)
        pass

        # replikation_dt
        replication_timestamp = timezone.localize(datetime.strptime(source_row['replikation_dt'], '%d.%m.%Y %H:%M:%S'))
        target_row['replication_date'] = replication_timestamp.isoformat(sep='T', timespec='auto')

        # sex
        pass

        # titre_dashboard2_d
        pass

        target_rows.append(target_row)

        target_rows.sort(key=lambda k:  k['case_number'])

    # for row in target_rows:
    #     print(row)

with open(args.target, 'w+', newline='', encoding='utf-8') as target_file:
    fieldnames = ['case_number', 'case_class', 'case_date', 'canton_abbr', 'gender', 'age_class', 'age', 'confirmed', 'confirmed_date', 'death', 'death_date', 'replication_date']
    writer = csv.DictWriter(target_file, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in target_rows:
        writer.writerow(row)
