#!/usr/bin/env python3

from typing import List
from abc import ABC, abstractmethod


class BssidResolver(ABC):
    @abstractmethod
    def resolve(self, bssids: List[str]) -> str:
        pass
