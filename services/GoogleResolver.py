#!/usr/bin/env python3

import urllib3
import requests
from models.ResolverResult import ResolverResult
from models.GpsPosition import GpsPosition
from services.BssidResolver import BssidResolver

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GoogleResolver(BssidResolver):
    CONTENT_TYPE_JSON = 'application/json'

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'accept': self.CONTENT_TYPE_JSON,
            'Content-Type': self.CONTENT_TYPE_JSON
        }
        self.endpoint = f'https://www.googleapis.com/geolocation/v1/geolocate?key={self.api_key}'

    def __get_payload(self, bssid: str):
        return {
            'considerIp': 'false',
            'wifiAccessPoints': [
                {'macAddress': bssid},
                {'macAddress': '00:25:9c:cf:1c:ad'} # dummy address
            ]
        }

    def __request(self, bssid: str, payload) -> ResolverResult:
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                verify=False
            )
            if response.status_code == 200:
                json = response.json()
                return ResolverResult(
                        'google',
                        bssid,
                        GpsPosition(json['location']['lat'],
                                    json['location']['lng'])
                        )
            else:
                #print('ELSE')
                return ResolverResult(
                    'google',
                    bssid,
                    None
                )
                # Return the error message in a dictionary
                #return {
                #    'module': 'google',
                #    'error': response.json()['error']['message']
                #}
        except Exception as e:
            print('ERROR')
            # Return the exception message in a dictionary
            return ResolverResult(
                'google',
                bssid,
                None
            )
            #return {
            #    'module': 'google',
            #    'error': str(e)
            #}

    def resolve(self, bssid: str) -> ResolverResult:
        payload = self.__get_payload(bssid)
        try:
            return self.__request(bssid, payload)
        except:
            print('oh')
            return None
