#!/usr/bin/env python3

from typing import List
from models.BssidLogEntry import BssidLogEntry
from models.ResolverResult import ResolverResult


class ResolvedBssidLogEntry:
    def __init__(self, log: BssidLogEntry, resolver_results: List[ResolverResult]):
        self.log = log
        self.resolver_results = resolver_results

    def __str__(self):
        return f"{self.log} {','.join(str(result) for result in self.resolver_results)}"
