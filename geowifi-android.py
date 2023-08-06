#!/usr/bin/env python3

import time
import argparse
from typing import List
from services.Banner import Banner
from services.LogParser import LogParser
from models.BssidLogEntry import BssidLogEntry
from services.BssidResolver import BssidResolver
from models.ResolverResult import ResolverResult
from services.AppleResolver import AppleResolver
from services.ResolverFactory import ResolverFactory
from models.ResolvedBssidLogEntry import ResolvedBssidLogEntry

print(Banner())

parser = argparse.ArgumentParser(description='Search for information about'
                                 + ' a network with a specific BSSID')
parser.add_argument('log_file', type=str, help='path to log file')
args = parser.parse_args()

log_parser = LogParser()
logs: List[BssidLogEntry] = log_parser.parse(args.log_file)
logs: List[BssidLogEntry] = log_parser.get_unique(logs)
logs: List[BssidLogEntry] = log_parser.sort_by_date(logs)

resolvers: List[BssidResolver] = [
  # GoogleResolver(''),
  AppleResolver()
]
factory = ResolverFactory(resolvers)

resolved_log_entries: List[ResolvedBssidLogEntry] = []
for log in logs:
    time.sleep(5)
    results: List[ResolverResult] = factory.resolve(log.bssid)
    print(ResolvedBssidLogEntry(log, results))
