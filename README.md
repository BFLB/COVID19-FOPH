# COVID19-FOPH
Covid-19 data scraped from Website of Federal Office of Public Health (BAG) of Switzerland

## Introduction
This repository contains covid-19 data files from Federal Office of Public Health (BAG) of Switzerland  
https://covid-19-schweiz.bagapps.ch/de-1.html


## Original files
Orignial files are stored in the directory data/tableau/converted

## Conveted files
In order to improve the usability of data, the files are availabled as well in converted, english version.
The following changes are applied:
- Remove columns which contain redundant information
- Translate column names and cell values to english
- Convert date values to iso-8601 format with timezone offset
- Convert fields with only 0/1 or N/A values to booleans
- Convert file endings to unix format
  
The files can be found in the directory data/tableau/converted

## Scraping
The files are not directly downloadable and scrapping is not easy as well. 
Thus the files are scraped and added to the repo manually. As soon as a scraping solution
exist, the process should be automated

## Converting
The original files can be converted with the convert-tableau-csv Python script in the rood directory of this repository.

## Contribution
Review, re-use, contribution or comments are highly welcome. If this could be integrated in a better known and maintained repository, it would be great.

## Disclaimer
This project has just started and is in a very early state and under development. Everything can change without warning. All data and sources of this repository are provided with no warranty. There is no guaranty that the data will be updated on a regular basis.
