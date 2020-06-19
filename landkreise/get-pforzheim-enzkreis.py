"""Parser for Pforzheim's Corona case numbers

This script parses the website of Pforzheim to extract the case numbers
of Pforzheim itself and Endkreis.

Return code:
* 1: if the parser could not extract the case number

"""
from bs4 import BeautifulSoup

import requests
import datetime
import re
import sys

import locale
locale.setlocale(locale.LC_TIME, "de_DE.utf-8")

import scrape
from helper import *
from database_interface import *

main_url = "https://www.enzkreis.de/Quicknavigation/Start/Gesundheitsamt-informiert-%C3%BCber-das-neue-Coronavirus-SARS-CoV-2-Fast-50-best%C3%A4tigte-F%C3%A4lle-in-Pforzheim-und-im-Enzkreis.php?object=tx,2891.6&ModID=7&FID=2891.1978.1"

req = scrape.request_url(main_url)
bs = BeautifulSoup(req.text, "html.parser")

cases_pforzheim_pattern = "Pforzheim gibt es \d+"
cases_enzkreis_pattern = "im Enzkreis \d+"

text=clear_text_of_ambigous_chars(bs.getText())
text=remove_chars_from_text(text,["\n"])

status_raw = re.findall("Stand: .* Uhr\)", text)
if not status_raw:
    # - early exist, because the regex did not match anything
    #   Possible reason: website changed the structure?
    sys.exit(1)
status= get_status(status_raw[0])


cases_pforzheim_raw = re.findall(cases_pforzheim_pattern,text)[0]
cases_pforzheim = int(re.findall(r'[0-9]+', cases_pforzheim_raw)[0])

cases_enzkreis_raw = re.findall(cases_enzkreis_pattern,text)[0]
cases_enzkreis = int(re.findall(r'[0-9]+', cases_enzkreis_raw)[0])


add_to_database("08231", status, cases_pforzheim, "Pforzheim")
add_to_database("08236", status, cases_enzkreis, "Enzkreis")
