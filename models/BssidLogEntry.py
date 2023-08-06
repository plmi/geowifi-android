#!/usr/bin/env python3

from __future__ import annotations
import re
import os
import errno
from datetime import datetime


class BssidLogEntry():
    def __init__(self, timestamp: datetime, bssid: str, ssid: str) -> None:
        self.timestamp = timestamp
        self.bssid = bssid
        self.ssid = ssid

    def __str__(self):
        return f"{self.timestamp.strftime('%H:%M:%S')} {self.bssid} {self.ssid}"

    def __eq__(self, other: BssidLogEntry):
        return self.bssid == other.bssid \
            and self.ssid == other.ssid
        #return self.timestamp == other.timestamp \
        #    and self.bssid == other.bssid \
        #    and self.ssid == other.ssid

    def __hash__(self):
        return hash(('bssid', self.bssid, 'ssid', self.ssid))
        #return hash(('timestamp', self.timestamp, 'bssid', self.bssid, 'ssid', self.ssid))

    @staticmethod
    def __substring(log_line: str, regex_pattern: str) -> str:
        match = re.search(regex_pattern, log_line)
        if match:
            return match.group(0)
        else:
            return None

    @staticmethod
    def create_from_log_line(log_line: str) -> BssidLogEntry:
        if not log_line:
            raise TypeError(errno.EINVAL,
                            os.strerror(errno.EINVAL), log_line)

        timestamp: datetime = datetime.strptime(log_line[0:15], '%H:%M:%S.%f')
        bssid: str = BssidLogEntry.__substring(log_line, r"([a-f0-9]{2}:){5}[a-f0-9]{2}")
        ssid: str = BssidLogEntry.__substring(log_line, r'"(.*)"')

        return BssidLogEntry(timestamp, bssid, ssid)
