#!/usr/bin/env python
import datetime
import logging
import certifi
import json
import requests
import os

fmp_api = os.environ.get('FMP_KEY')

def get_jsonparsed_data(url):
    response = requests.get(url, verify=certifi.where())
    data = response.text
    return json.loads(data)

def get_cached_fetch(url, filename):
    now = datetime.datetime.now()
    quarter = (now.month - 1) // 3 + 1
    year = now.year
    currentquarteryear = (year, quarter)
    filename = filename + str(currentquarteryear)
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            j = json.load(f)
            return j
    j = get_jsonparsed_data(url)
    with open(filename, 'w') as f:
        json.dump(j, f)
    return j

def get_transcript(ticker, year, quarter):
    logging.info("Getting transcript for " + ticker)
    filename = f"../Data/DataCache/{ticker}_{year}_{quarter}.json"
    url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{ticker}?year={year}&quarter={quarter}&apikey={fmp_api}"
    j = get_cached_fetch(url, filename)
    if not j:
        return ""
    return j[0]['content']
