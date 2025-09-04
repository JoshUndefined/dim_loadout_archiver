# Helper class to connect to Bungie.net API

import os
from localStoragePy import localStoragePy
import requests
import json
from lib.d2manifest import D2Manifest

class DestinyAPI_Credentials:
    def __init__(self, client_id=None, client_secret=None, api_key=None, redirect_uri=None):
        if(client_id is None or client_secret is None or redirect_uri is None):
            self.client_id = os.environ.get("BUNGIE_CLIENT_ID")
            self.client_secret = os.environ.get("BUNGIE_CLIENT_SECRET")
            self.api_key = os.environ.get("BUNGIE_API_KEY")
            self.redirect_uri = os.environ.get("BUNGIE_CLIENT_SECRET")
        else:
            self.client_id = client_id
            self.client_secret = client_secret
            self.api_key = api_key
            self.redirect_uri = redirect_uri

class DestinyAPI:
    def __init__(self, manifest, credentials = DestinyAPI_Credentials(), verbose = False):
        self.manifest = manifest
        self.credentials = credentials

    def authorize(self):
        # TODO: handle auth tokens and refreshing using localstorage, for now it's in .env
        self.access_token = self.refresh_token(os.environ.get("TEMP_REFRESH_TOKEN")).get("access_token")

    def exchange_code(self, code):
        data = {
            'client_id': self.credentials.client_id,
            'client_secret': self.credentials.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post("https://www.bungie.net/platform/app/oauth/token/", data=data, headers=headers)
        r.raise_for_status()
        return r.json()

    def refresh_token(self, refresh_token):
        data = {
            'client_id': self.credentials.client_id,
            'client_secret': self.credentials.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post("https://www.bungie.net/platform/app/oauth/token/", data=data, headers=headers)
        r.raise_for_status()
        return r.json()
    
    def bnet_get_item(self, item_id):
        headers = {
            'X-API-Key': self.credentials.api_key,
            'Authorization': f"Bearer {self.access_token}"
        }
        # print(self.credentials.api_key)
        # print( f"Bearer {access_token}")
        # print(item_id)
        url = f"https://www.bungie.net/Platform/Destiny2/2/Profile/4611686018446045242/Item/{item_id}?components=305,310"
        r = requests.request("GET", url=url, headers=headers)
        try:
            r.raise_for_status()
        except:
            pass
        return r.json()

    def get_instanced_item(self, item_id, hash, pretty=True):
        return_data = {}
        return_data["hash"] = hash
        return_data["id"] = item_id
        
        # Instanced item available perks by socket
        reusable_plugs_raw = self.bnet_get_item(item_id).get("Response", {}).get("reusablePlugs", {}).get("data", {}).get("plugs", {})
        # return_data["reusable_plugs_raw"] = reusable_plugs_raw # DEBUG


        data = self.manifest.get_definition("DestinyInventoryItemDefinition", hash)
        if data is None:
            return_data["error"] = f"item hash {hash} does not exist in manifest. Check manifest version."
            return json.dumps(return_data, indent=2) if pretty else return_data
        
        data = self.manifest.get_definition("DestinyInventoryItemDefinition", hash).get("sockets", {})
        # From socketCategories[], get a list of socketIndexes where socketCategoryHash = 4241085061 (Weapon Perks)
        socketIndexes = []
        socketCategories_raw = data.get("socketCategories")
        if(socketCategories_raw):
            for category in socketCategories_raw:
                if category.get("socketCategoryHash") == 4241085061: # Weapon Perks
                    socketIndexes = category.get("socketIndexes", [])
                    # return_data["socketIndexes"] = socketIndexes # DEBUG
        for i in socketIndexes:
            perks = []
            for perk in reusable_plugs_raw.get(str(i), {}):
                perk_name = self.manifest.get_weapon_perk(perk.get("plugItemHash")).get("displayProperties", {}).get("name", {}) # TESTING, Just get the perk name for now
                perks.append(perk_name)
            if perks != []:
                return_data["socket " + str(i)] = perks



        return json.dumps(return_data, indent=2) if pretty else return_data