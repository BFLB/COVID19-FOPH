# COVID19-FOPH
Covid-19 data scraped from Website of Federal Office of Public Health (BAG) of Switzerland

## Introduction
This repository contains covid-19 data files from Federal Office of Public Health (BAG) of Switzerland  
https://covid-19-schweiz.bagapps.ch/de-1.html


## Original files
Orignial files are stored in the directory data/original/

## Conveted files
In order to improve the usability of data, the files are available as well in converted versions
The following changes are applied:
- Remove columns which contain redundant information
- Translate column names and cell values to english
- Convert date values to iso-8601 format with timezone offset
- Convert fields with only 0/1 or N/A values to booleans
- Add country and canton names in abbreviated, german and english
- Add country and canton gps location
- Convert file endings to unix format

The converted files are located in data/converted

## data_processor.py
data_processor is a Pyhton command line tool to scrap / convert and git-push the data

## Roadmap
- Convert:
  - lean file (only non zero datasets)

- Implement test data (Available on FOPH Site since beginning of may)

## Contribution
Review, re-use, contribution or comments are highly welcome. If this could be integrated in a better known and maintained repository, it would be great.

## Disclaimer
This project has just started and is in a very early state and under development. Everything can change without warning. All data and sources of this repository are provided with no warranty. There is no guaranty that the data will be updated on a regular basis.
