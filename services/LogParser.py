#!/usr/bin/env python3

import os
import errno
from typing import List
from models.BssidPredicate import BssidPredicate
from models.BssidLogEntry import BssidLogEntry


class LogParser():
    def sort_by_date(self, logs: List[BssidLogEntry]) -> List[BssidLogEntry]:
        return sorted(logs, key=lambda x: x.timestamp)

    def get_unique(self, logs: List[BssidLogEntry]) -> List[BssidLogEntry]:
        return list(set(logs))

    def parse(self, log_file: str) -> List[BssidLogEntry]:
        if not log_file:
            raise TypeError(errno.EINVAL,
                            os.strerror(errno.EINVAL), log_file)
        if not os.path.isfile(log_file):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT), log_file)

        logs: List[BssidLogEntry] = [BssidLogEntry.create_from_log_line(line)
                                     for line in self.__readAllLines(
                                         log_file, BssidPredicate.get())]
        return logs

    def __readAllLines(self, log_file: str, predicate: callable) -> List[str]:
        with open(log_file) as file:
            lines = file.read().splitlines()
            return list(filter(predicate, lines))
