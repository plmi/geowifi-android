#!/usr/bin/env python3

from typing import List
from services.BssidResolver import BssidResolver
from models.ResolverResult import ResolverResult


class ResolverFactory:
    def __init__(self, resolvers: List[BssidResolver]):
        self.resolvers = resolvers

    def resolve(self, bssid: str) -> List[ResolverResult]:
        resolver_results: List[ResolverResult] = []
        for resolver in self.resolvers:
            resolver_result: ResolverResult = resolver.resolve(bssid)
            resolver_results.append(resolver_result)

        return resolver_results
