#!/usr/bin/env python3
import subprocess
import argparse
from collections import defaultdict
from enum import Enum
import os
import time
import requests
from bs4 import BeautifulSoup

class RegionEnum(str, Enum):
    NA = 'AM'
    EU = 'EU'
    KR = 'KR'
    
def _get_league_id(region: RegionEnum, edition: int):
    if region == 'AM':
       region2 = "americas"
    if region == 'EU':
       region2 = "europe"
    if region == 'KR':
       region2 = "korea"
    url = 'http://localhost:8191/v1'
    payload = {
            'cmd': 'request.get',
            'url': 'https://play.eslgaming.com/starcraft/global/sc2/open/1on1-series-' + region2 + '/cup-' + str(edition),
             'maxTimeout': 60000,
    }
    res = requests.post(url, json=payload)
    soup = BeautifulSoup(res.content, "html.parser")
    section = soup.find('league-interaction')
    league_id = int("".join(filter(str.isdigit, section["league_id"])))
    os.environ["league_id"] = str(league_id)
    
def create_parser():
    parser = argparse.ArgumentParser(prog='shell')
    parser.add_argument('-n', '--dry_run', action='store_true',
                        help='Do not write anything; print on stdout instead')
    default_page = 'ESL_Open_Cup_${region}/${edition}'
    parser.add_argument('-p', '--page-template',
                        default=default_page,
                        help='Liquipedia page to edit. ' 
                            f'Defaults to "{default_page}"')
    parser.add_argument('region',
                        choices=[region.value for region in RegionEnum],
                        help='Region we are interested in')
    parser.add_argument('edition',
                        type=int,
                        help='Edition we are interested in')
    return parser
    
def main():
    parser = create_parser()
    args = parser.parse_args()
    _get_league_id(args.region, args.edition)
    x = range(240)
    if args.dry_run == True:
        subprocess.run(["python", "lp_ept_cups.py", "-n", "-p", args.page_template, "participants", args.region, str(args.edition)])
        time.sleep(60)
        for n in x:
            subprocess.run(["python", "lp_ept_cups.py", "-n", "-p", args.page_template, "results", args.region, str(args.edition)])
            time.sleep(60)
    else:
        subprocess.run(["python", "lp_ept_cups.py", "-p", args.page_template, "participants", args.region, str(args.edition)])
        time.sleep(60)
        for n in x:
            subprocess.run(["python", "lp_ept_cups.py", "-p", args.page_template, "results", args.region, str(args.edition)])
            time.sleep(60)
        
if __name__ == '__main__':
    main()
