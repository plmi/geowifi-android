#!/usr/bin/env python3

class BssidPredicate():
    def get() -> callable:
        def predicate(text: str):
            return 'scan] Received prb' in text
        return predicate
