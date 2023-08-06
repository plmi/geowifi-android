#!/usr/bin/env python3

class GpsPosition:
    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        self._latitude = value

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        self._longitude = value

    def __str__(self):
        return f"({self._latitude}:{self._longitude})"
