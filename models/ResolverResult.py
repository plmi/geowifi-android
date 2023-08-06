#!/usr/bin/env python3

from typing import Optional
from models.GpsPosition import GpsPosition


class ResolverResult:
    def __init__(self, module: str, bssid: str, position: Optional[GpsPosition]):
        self.module = module
        self.bssid = bssid
        self.position = position

    def __str__(self):
        #return f"{self.module} {self.position}"
        return f"{self.position}"
