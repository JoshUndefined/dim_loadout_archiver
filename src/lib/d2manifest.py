# Helper class to get data from D2 manifest

import json
import sqlite3
from pathlib import Path

class D2Manifest:
    def __init__(self, manifest_path, verbose = False):
        self._manifest_path = manifest_path
        conn = sqlite3.connect(manifest_path)
        self._cur = conn.cursor()
        self.verbose = verbose

    def get_inventory_item(self, hash, pretty = True):
        data = self.get_definition("DestinyInventoryItemDefinition", hash)
        return_data = {}
        return_data["hash"] = hash

        displayProperties_raw = data.get("displayProperties", {})
        displayProperties = {
            "name": displayProperties_raw.get("name"),
            "description": displayProperties_raw.get("description"),
            "icon": "https://bungie.net" + displayProperties_raw.get("icon")
        }
        # if(self.verbose): displayProperties["displayProperties_raw"] = displayProperties_raw
        return_data["displayProperties"] = displayProperties

        damageTypes_raw = data.get("damageTypeHashes")
        if(damageTypes_raw):
            damageTypes = []
            for damageType in damageTypes_raw:
                if(self.verbose):
                    damageTypes.append(f"[{damageType}] {self.get_damage_type(damageType)}")
                else:
                    damageTypes.append(self.get_damage_type(damageType))
            return_data["damageTypes"] = damageTypes

        flavorText = data.get("flavorText")
        return_data["flavorText"] = flavorText

        inventory_raw = data.get("inventory")
        inventory = {}
        # if(inventory_raw.get("recoveryBucketTypeHash")):
        #     inventory["recoveryBucketType"] = self.get_inventory_bucket(inventory_raw.get("recoveryBucketTypeHash"))
        #     if(self.verbose):
        #         inventory["recoveryBucketType"]["recoveryBucketTypeHash"] = inventory_raw.get("recoveryBucketTypeHash")
        if(inventory_raw.get("bucketTypeHash")):
            inventory["bucketType"] = self.get_inventory_bucket(inventory_raw.get("bucketTypeHash"))
            if(self.verbose):
                inventory["bucketType"]["bucketTypeHash"] = inventory_raw.get("bucketTypeHash")
        if(inventory_raw.get("tierTypeHash")):
            inventory["tierType"] = self.get_item_tier_type(inventory_raw.get("tierTypeHash"))
            if(self.verbose):
                inventory["tierTypeHash"] = inventory_raw.get("tierTypeHash")
        return_data["inventory"] = inventory

        investmentStats_raw = data.get("investmentStats")
        if(investmentStats_raw):
            investmentStats = {}
            for investmentStat in investmentStats_raw:
                key = self.get_stat_type(investmentStat.get("statTypeHash"))
                if(key):
                    key = key.get("displayProperties").get("name")
                    if(self.verbose): key = f"[{investmentStat.get('statTypeHash')}] {key}"
                    investmentStats[key] = investmentStat.get("value")
            return_data["investmentStats"] = investmentStats

        itemCategories_raw = data.get("itemCategoryHashes")
        itemCategories = []
        for itemCategory in itemCategories_raw:
            desc = self.get_item_category_type(itemCategory).get("displayProperties").get("name")
            if(self.get_item_category_type(itemCategory).get("displayProperties").get("description")):
                desc = desc + ": " + self.get_item_category_type(itemCategory).get("displayProperties").get("description")
            itemCategories.append(desc)
        return_data["itemCategories"] = itemCategories
        if(self.verbose): return_data["itemCategoryHashes"] = itemCategories_raw

        if(data.get("screenshot")):
            screenshot = "https://bungie.net" + data.get("screenshot")
            return_data["screenshot"] = screenshot

        traits_raw = data.get("traitHashes")
        if(traits_raw):
            traits = []
            for trait in traits_raw:
                if(self.get_trait(trait)):
                    trait_data = {}
                    trait_data["name"] = self.get_trait(trait).get("name")
                    trait_data["description"] = self.get_trait(trait).get("description")
                    trait_data["icon"] = "https://bungie.net" + self.get_trait(trait).get("icon")
                    if(self.verbose): trait_data["traitHash"] = trait
                    traits.append(trait_data)
                    # traits.append(self.get_trait(trait))
            return_data["traits"] = traits

        perks_raw = data.get("perks")
        if(perks_raw):
            perks = []
            for perk in perks_raw:
                if(self.get_sandbox_perk(perk.get("perkHash"))):
                    perk_data = {}
                    perk_data["name"] = self.get_sandbox_perk(perk.get("perkHash")).get("name")
                    perk_data["description"] = self.get_sandbox_perk(perk.get("perkHash")).get("description")
                    perk_data["icon"] = "https://bungie.net" + self.get_sandbox_perk(perk.get("perkHash")).get("icon")
                    if(self.verbose): perk_data["perkHash"] = perk.get("perkHash")
                    perks.append(perk_data)
            return_data["perks"] = perks

        return json.dumps(return_data, indent=2) if pretty else return_data

    def get_definition(self, table, hash):
        self._cur.execute(
            f"SELECT json FROM {table} WHERE id = ?",
            (self._d2_hash(hash),)
            )
        row = self._cur.fetchone()
        if row:
            try:
                data = json.loads(row[0])
                return data
            except json.JSONDecodeError:
                return None
        return None

    def get_inventory_bucket(self, hash):
        data = self.get_definition("DestinyInventoryBucketDefinition", hash)
        return {
            "name": data.get("displayProperties", {}).get("name"),
            "description": data.get("displayProperties", {}).get("description")
        }

    def get_loadout_color(self, hash):
        return self.get_definition("DestinyLoadoutColorDefinition", hash)

    def get_loadout_icon(self, hash):
        return self.get_definition("DestinyLoadoutIconDefinition", hash)

    def get_loadout_name(self, hash):
        return self.get_definition("DestinyLoadoutNameDefinition", hash)

    def get_damage_type(self, hash):
        return self.get_definition("DestinyDamageTypeDefinition", hash).get("displayProperties", {}).get("name")

    def get_item_tier_type(self, hash):
        return self.get_definition("DestinyItemTierTypeDefinition", hash).get("displayProperties", {}).get("name")

    def get_item_category_type(self, hash):
        return self.get_definition("DestinyItemCategoryDefinition", hash)#.get("displayProperties", {}).get("name")

    def get_stat_type(self, hash):
        if(hash == 1885944937): # this one is nothing
            return None
        return self.get_definition("DestinyStatDefinition", hash)#.get("displayProperties", {}).get("name")

    def get_trait(self, hash):
        data = self.get_definition("DestinyTraitDefinition", hash).get("displayProperties", {})
        if(data.get("name") == ""):
            return None
        return {
            "name": data["name"],
            "description": data["description"],
            "icon": data["icon"]
        }
    
    def get_sandbox_perk(self, hash):
        data = self.get_definition("DestinySandboxPerkDefinition", hash)#.get("displayProperties", {})
        if(not data.get("isDisplayable")):
            return None
        data = data.get("displayProperties", {})
        return {
            "name": data["name"],
            "description": data["description"],
            "icon": data["icon"]
        }
    
    def get_weapon_perk(self, hash):
        data = self.get_definition("DestinyInventoryItemDefinition", hash)
        return data
    
    def get_curated_weapon(self, hash, pretty = True):
        data = self.get_definition("DestinyInventoryItemDefinition", hash).get("sockets", {})
        return_data = {}
        return_data["hash"] = hash

        # return_data["raw_data_test"] = data#.get("socketCategories")

        # From socketCategories[], get a list of socketIndexes where socketCategoryHash = 4241085061 (Weapon Perks)
        socketCategories_raw = data.get("socketCategories")
        if(socketCategories_raw):
            for category in socketCategories_raw:
                if category.get("socketCategoryHash") == 4241085061: # Weapon Perks
                    socketIndexes = category.get("socketIndexes", [])
                    # return_data["socketIndexes"] = socketIndexes

        # For Curated roll: socketEntries[socketIndexes[...]].singleInitialItemHash
        socketEntries_raw = data.get("socketEntries", [])
        socketEntries = []
        for i in socketIndexes:
            socketEntries.append(self.get_weapon_perk(socketEntries_raw[i].get("singleInitialItemHash")))
        # return_data["perks"] = socketEntries
        perks = []
        for perk in socketEntries:
            perks.append(perk.get("displayProperties", {}).get("name"))
        return_data["curatedPerks"] = perks


        # TODO: intrinsic maybe didn't work as expected?
        # intrinsic = data.get("intrinsicSockets", [])[0].get("plugItemHash")
        # return_data["intrinsic"] = self.get_weapon_perk(intrinsic)

        # intrinsics_raw = data.get("intrinsicSockets")
        # if(intrinsics_raw):
        #     intrinsics = []
        #     for intrinsic in intrinsics_raw:
        #         if(self.get_weapon_perk(intrinsic.get("plugItemHash"))):
        #             intrinsic_data = {}
        #             intrinsic_data["rawtest"] = self.get_weapon_perk(intrinsic.get("plugItemHash"))
        #             if(self.verbose): intrinsic_data["plugItemHash"] = intrinsic.get("plugItemHash")
        #             intrinsics.append(intrinsic_data)
        #     return_data["intrinsics"] = intrinsics

        return json.dumps(return_data, indent=2) if pretty else return_data

    # SQlite3 IDs are Signed Int, D2 Hash are Unsigned Int
    def _d2_hash(self, hash):
        return hash - 2**32 if hash > 0x7FFFFFFF else hash