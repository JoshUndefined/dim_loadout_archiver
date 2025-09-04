# Helper class to connect to Bungie.net API

from dotenv import load_dotenv
from localStoragePy import localStoragePy
import requests
import json

class DestinyAPI_Credentials:
    def __init__(self):
        self.client_id = ""
        self.client_secret = ""

class DestinyAPI:
    def __init__(self, credentials, verbose = False):
        pass