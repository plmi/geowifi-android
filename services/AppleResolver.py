#!/usr/bin/env python3

import re
import requests
from models.GpsPosition import GpsPosition
from models.BSSIDApple_pb2 import BSSIDResp
from google.protobuf.message import DecodeError
from models.ResolverResult import ResolverResult
from services.BssidResolver import BssidResolver


class AppleResolver(BssidResolver):
    def __init__(self):
        self.name = 'apple'
        self.endpoint = 'https://gs-loc.apple.com/clls/wloc'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-us',
            'User-Agent': 'locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0'
        }

    def __get_payload(self, bssid: str):
        encoded_bssid = f'\x12\x13\n\x11{bssid}\x18\x00\x20\01'
        return '\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a' \
            + '8.1.12B411\x00\x00\x00\x01\x00\x00\x00' + \
            chr(len(encoded_bssid)) + encoded_bssid

    def __parse_response_to_protobuf(self, response):
        bssid_response = BSSIDResp()
        try:
            return bssid_response.ParseFromString(response.content[10:])
        except DecodeError as e:
            return f'Failed to decode response: {e}'

    def __extract_gps_position(self, bssid_response):
        try:
            lat_match = re.search('lat: (\S*)', str(bssid_response))
            lon_match = re.search('lon: (\S*)', str(bssid_response))
            lat = lat_match.group(1)
            lon = lon_match.group(1)
            if '18000000000' not in lat:
                lat = float(lat[:-8] + '.' + lat[-8:])
                lon = float(lon[:-8] + '.' + lon[-8:])
                return GpsPosition(lat, lon)
            else:
                return {
                    'module': 'apple',
                    'error': 'Latitude or longitude value not found in response'
                }
        except Exception as e:
            if not lat_match or not lon_match:
                # Return the error message in a dictionary
                return {
                    'module': 'apple',
                    'error': 'Latitude or longitude value not found in response'
                }
            # Return the exception message in a dictionary
            return {
                'module': 'apple',
                'error': str(e)
            }

    def __request(self, bssid: str, payload) -> ResolverResult:
        return requests.post(
            self.endpoint,
            headers=self.headers,
            data=self.__get_payload(bssid),
            verify=False)


    def resolve(self, bssid: str) -> ResolverResult:
        """Searches for a network with a specific BSSID in the Apple database.

        Parameters:
            bssid_param (str): The BSSID of the network to search for.

        Returns:
            dict: A dictionary containing information about the network, or an error message if an error occurred.
        """

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-us',
            'User-Agent': 'locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0'
        }

        # Set up the POST data
        data_bssid = f'\x12\x13\n\x11{bssid}\x18\x00\x20\01'
        data = '\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a' + '8.1.12B411\x00\x00\x00\x01\x00\x00\x00' + chr(
            len(data_bssid)) + data_bssid
        # Set the endpoint for the request
        endpoint = 'https://gs-loc.apple.com/clls/wloc'
        # Make the HTTP POST request using the requests library
        response = requests.post(
            endpoint,
            headers=headers,
            data=data,
            verify=False)

        # Parse the binary content of the response into a BSSIDResp protobuf object.
        bssid_response = BSSIDResp()
        try:
            bssid_response.ParseFromString(response.content[10:])
        except DecodeError as e:
            return f'Failed to decode response: {e}'
        lat_match = re.search('lat: (\S*)', str(bssid_response))
        lon_match = re.search('lon: (\S*)', str(bssid_response))
        try:
            # Extract the latitude and longitude values from the response
            lat = lat_match.group(1)
            lon = lon_match.group(1)

            if '18000000000' not in lat:
                # format the latitude and longitude values
                lat = float(lat[:-8] + '.' + lat[-8:])
                lon = float(lon[:-8] + '.' + lon[-8:])
                return ResolverResult(
                  self.name,
                  bssid,
                  GpsPosition(lat, lon)
                )
            else:
                return ResolverResult(
                  self.name,
                  bssid,
                  None
                )
        except Exception as e:
            print(e)
            if not lat_match or not lon_match:
                return ResolverResult(
                  self.name,
                  bssid,
                  None
                )

            return ResolverResult(
              self.name,
              bssid,
              None
            )
