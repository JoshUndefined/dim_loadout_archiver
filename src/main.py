import sys
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from lib.d2manifest import D2Manifest
from lib.d2api import DestinyAPI

def main():
    parser = argparse.ArgumentParser(
        description="DIM Loadout Archiver"
    )
    # parser.add_argument("", help="", type=str)
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()

    logging.basicConfig(
        level = logging.DEBUG if args.verbose else logging.INFO,
        # format="%(asctime)s %(levelname)8s: %(message)s",
        # format="\033[95m%(asctime)s %(levelname)8s:\033[0m\n %(message)s",
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info("DIM Loadout Archiver")
    logger.debug("Verbose logging enabled")

    bnet = DestinyAPI()
    bnet.authorize()
    
    # TODO: Download the manifest locally instead
    manifest = D2Manifest(Path.cwd() / "data/manifest.db", verbose=args.verbose)

    with open("data/dim-api_loadouts_20250711-0854.json") as f: # DEBUG: Hard coded file name for now
        dim_loadouts = json.load(f)
        # logger.info(dim_loadouts)
    
    # print(dim_loadouts["sync"])
    # print(dim_loadouts["loadouts"])
    # print(dim_loadouts["syncToken"])

    # test(manifest=manifest)
    
    for loadout in dim_loadouts["loadouts"]:
        # DEBUG look at a specific loadout
        # if loadout["id"] != "015918bc-a732-4c27-b8f2-54d708b67424":
        # if loadout["id"] != "016b1049-9650-436b-8624-bc6fad245911":
        if loadout["id"] != "01c98aec-2173-404d-8094-dca10f0caa2b": 
        # if loadout["id"] != "7ffe28ce-c867-4481-9cf3-d87860d36d45": 
            continue
            
        logger.info(f"-------------------------------------------\nLoadout {loadout['id']} {loadout['name']}")
        # logger.info(loadout) # DEBUG https://github.com/DestinyItemManager/dim-api/blob/master/api/shapes/loadouts.ts

        logger.info("\n-------------------------------------------\n-----info:\n")
        logger.info(f"DIM id: {loadout.get('id')}")
        logger.info(f"name: {loadout.get('name')}")
        logger.info(f"classType: {loadout.get('classType')}")
        logger.info(f"createdAt: {loadout.get('createdAt')}")
        logger.info(f"lastUpdatedAt: {loadout.get('lastUpdatedAt')}")
        logger.info(f"notes: {loadout.get('notes')}")
        if "inGameIdentifiers" in loadout.get("parameters", {}).keys():
            inGameIdentifier = loadout["parameters"]["inGameIdentifiers"]
            logger.info("inGameLoadoutColor: https://bungie.net/" + manifest.get_loadout_color(inGameIdentifier["colorHash"]).get("colorImagePath"))
            logger.info("inGameLoadoutIcon: https://bungie.net/" + manifest.get_loadout_icon(inGameIdentifier["iconHash"]).get("iconImagePath"))
            logger.info("inGameLoadoutName: " + manifest.get_loadout_name(inGameIdentifier["nameHash"]).get("name"))
        else:
            logger.info("loadout.parameters.inGameIdentifiers does not exist")
    
        logger.info("\n-------------------------------------------\n-----equipped:\n")
        if "equipped" in loadout.keys():
            for equipped in loadout["equipped"]:
                logger.info("Manifest info: " + manifest.get_inventory_item(equipped["hash"]))
                # TODO for weapons:
                '''
                - Get item hash and instance from the loadout
                - Use the hash in Manifest to get the weapon
                    - From socketCategories[], get a list of socketIndexes where socketCategoryHash = 4241085061 (Weapon Perks)
                    - For Curated roll: socketEntries[socketIndexes[...]].singleInitialItemHash
                - Get instancedItem from D2 API with ?components=305,310 (ItemSockets & ItemReusablePlugs)
                    - If it doesn't exist, use the Curated Roll above
                    - Response.sockets.data.sockets[socketIndexes[]] has the current plug configuration
                    - Response.reusableSockets.data.plugs[socketIndexes[]] has every socket available plug
                '''
                logger.info("Curated weapon roll: " + manifest.get_curated_weapon(equipped["hash"]))
                # TODO: Get instanced item details
                logger.info("Item Instance ID: " + equipped.get("id"))
                r = bnet.get_instanced_item(equipped.get("id"), False)
                logger.info(r)
                craftedDate = equipped.get("craftedDate")
                if craftedDate:
                    logger.info("Crafted: " + datetime.fromtimestamp(craftedDate).strftime("%Y-%m-%d %H:%M:%S UTC"))

                if "socketOverrides" in equipped.keys():
                # Subclass selectable details like Super, Aspects, Abilities
                    logger.info("\n-------------------------------------------\n-----socketOverrides:\n")
                    for subclass in equipped["socketOverrides"].values():
                        logger.info(manifest.get_inventory_item(subclass))
        else:
            logger.info("loadout.equipped does not exist")

        logger.info("\n-------------------------------------------\n-----unequipped:\n")
        if "unequipped" in loadout.keys():
            for unequipped in loadout["unequipped"]:
                logger.info("Manifest info: " + manifest.get_inventory_item(unequipped["hash"]))
                logger.info("Curated weapon roll: " + manifest.get_curated_weapon(unequipped["hash"]))
                # TODO: Get instanced item details
                logger.info("Item Instance ID: " + unequipped.get("id"))
                r = bnet.get_instanced_item(unequipped.get("id"), False)
                logger.info(r)
                craftedDate = unequipped.get("craftedDate")
                if craftedDate:
                    logger.info("Crafted: " + datetime.fromtimestamp(craftedDate).strftime("%Y-%m-%d %H:%M:%S UTC"))
        else:
            logger.info("loadout.unequipped does not exist")

        logger.info("\n-------------------------------------------\n-----mods:\n")
        # These are "loose" armor mods set in DIM that the DIM loadout generator will assign to armor
        if "mods" in loadout.get("parameters", {}).keys():
            for mod in loadout["parameters"]["mods"]:
                logger.info(manifest.get_inventory_item(mod))
        else:
            logger.info("loadout.parameters.mods does not exist")

        logger.info("\n-------------------------------------------\n-----mods by bucket:\n")
        if "modsByBucket" in loadout.get("parameters", {}).keys():
            # Cosmetic armor mods by armor slot
            for inventoryBucket in loadout["parameters"]["modsByBucket"]:
                logger.info(f"-- Bucket: {manifest.get_inventory_bucket(int(inventoryBucket))}")
                for mod in loadout["parameters"]["modsByBucket"][inventoryBucket]:
                    # logger.info(mod)
                    logger.info(manifest.get_inventory_item(mod))
        else:
            logger.info("loadout.parameters.modsByBucket does not exist")

        logger.info("\n-------------------------------------------\n-----artifactUnlocks:\n")
        if "artifactUnlocks" in loadout.get("parameters", {}).keys():
            # Seasonal artifact mods
            for artifactMod in loadout["parameters"]["artifactUnlocks"]["unlockedItemHashes"]:
                # logger.info(artifactMod)
                logger.info(manifest.get_inventory_item(artifactMod))
        else:
            logger.info("loadout.parameters.artifactUnlocks does not exist")

        # break # DEBUG just running the first found loadout for now



def test(manifest):
    ######################
    # Below are just tests to get a better understanding of the way sockets and plugs work for weapons
    # Hash values are manually grabbed from a call to Destiny2.GetItem API endpoint
    # "id": "0025a7a6-08b0-4e7d-9ac5-5e73f0b7f71b",
    # "name": "S25 Solo GM Birthplace Healing",

    logger.info("-------\nInstanced Item (Kinetic) Exotic 2357297366 6917529570267995779")
    logger.info(manifest.get_inventory_item(2357297366))
    logger.info(manifest.get_curated_weapon(2357297366))
    # logger.info("Response: sockets: data: sockets: ")
    # logger.info(manifest.get_inventory_item(3063320916))
    # logger.info(manifest.get_inventory_item(3809316345))
    # logger.info(manifest.get_inventory_item(1996142143))
    # logger.info(manifest.get_inventory_item(745965939))
    # logger.info(manifest.get_inventory_item(3465198467))
    # logger.info("null")
    # logger.info(manifest.get_inventory_item(2931483505))
    # logger.info("null")
    # logger.info("null")
    # logger.info(manifest.get_inventory_item(2302094943))
    # logger.info(manifest.get_inventory_item(2888418988))

    # logger.info("-------\nInstanced Item (Energy) 859869931 6917530072495898329")
    logger.info(manifest.get_inventory_item(859869931))
    logger.info(manifest.get_curated_weapon(859869931))
    logger.info("Not found")

    logger.info("-------\nInstanced Item (Power) Crafted VS Chill Inhibitor 1762785662 6917530072480039762")
    logger.info(manifest.get_inventory_item(1762785662))
    logger.info(manifest.get_curated_weapon(1762785662))
    # # ########################################################
    # logger.info("Response: sockets: data: sockets: ") # Current configuration
    # logger.info(manifest.get_inventory_item(762801111)) # Rapid-fire frame; socket 0
    # logger.info(manifest.get_inventory_item(1844523823)) # Confined Launch; socket 1
    # logger.info(manifest.get_inventory_item(3301904089)) # Spike Grenades; socket 2
    # logger.info(manifest.get_inventory_item(331667533)) # Cascade Point; socket 3
    # logger.info(manifest.get_inventory_item(3744057135)) # Bait and Switch; socket 4
    # logger.info(manifest.get_inventory_item(4248210736)) # Default Shader; socket 5
    # logger.info(manifest.get_inventory_item(3336648220)) # Backup Mag; socket 6
    # # logger.info(manifest.get_inventory_item(233125175)) # fails on no icon image, isVisible = false; socket 7
    # logger.info(manifest.get_inventory_item(4139916815)) # Bray Legacy; socket 8
    # logger.info(manifest.get_inventory_item(2240097604)) # Kill Tracker; socket 9
    # logger.info(manifest.get_inventory_item(2215619028)) # null, isVisible = false; socket 10
    # logger.info(manifest.get_inventory_item(2909846572)) # Empty Memento Socket; socket 11
    # logger.info(manifest.get_inventory_item(2728416796)) # Tier 3 Enhancement, this one has investmentStats which is +10 for each stat; socket 12
    # logger.info(manifest.get_inventory_item(4043342755)) # Empty Weapon Level Boost Socket; socket 13
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 1: ")
    # logger.info(manifest.get_inventory_item(1844523823)) # Confined Launch EQUIPPED
    # logger.info(manifest.get_inventory_item(1441682018)) # Linear Compensator
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 2: ")
    # logger.info(manifest.get_inventory_item(3301904089)) # Spike Grenades EQUIPPED
    # logger.info(manifest.get_inventory_item(1771897777)) # Augmented Drum
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 3: ")
    # logger.info(manifest.get_inventory_item(331667533)) # Cascade Point EQUIPPED
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 4: ")
    # logger.info(manifest.get_inventory_item(3744057135)) # Bait and Switch EQUIPPED
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 5: ") ## selectable memento socket
    # logger.info(manifest.get_inventory_item(1545278261))
    # logger.info(manifest.get_inventory_item(3387636832))
    # logger.info(manifest.get_inventory_item(3387636833))
    # logger.info(manifest.get_inventory_item(412487139))
    # logger.info(manifest.get_inventory_item(412487138))
    # logger.info(manifest.get_inventory_item(2117628185))
    # logger.info(manifest.get_inventory_item(1559478790))
    # logger.info(manifest.get_inventory_item(3510413604))
    # logger.info(manifest.get_inventory_item(195075337))
    # logger.info(manifest.get_inventory_item(195075336))
    # logger.info(manifest.get_inventory_item(195075339))
    # logger.info(manifest.get_inventory_item(4248210736)) # EQUIPPED
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 6: ") # selectable weapon mods available
    # logger.info(manifest.get_inventory_item(2400144052)) # Tactical
    # logger.info(manifest.get_inventory_item(2254149382)) # Aerodynamics
    # logger.info(manifest.get_inventory_item(3159358855)) # Anti-Flinch
    # # ...
    # logger.info(manifest.get_inventory_item(3336648220)) # Backup Mag EQUIPPED
    # # ...
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 7: ") # masterworks available? enhanced weapon, might not be in use
    # logger.info(manifest.get_inventory_item(1590375901)) # Tier 1: Stability
    # logger.info(manifest.get_inventory_item(150943607)) # Tier 1: Range
    # logger.info(manifest.get_inventory_item(518224747)) # Tier 1: Handling
    # # ...
    # logger.info(manifest.get_inventory_item(3673787993)) # Tier 1: Shield Duration
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 9: ") # 
    # logger.info(manifest.get_inventory_item(2285636663)) # Crucible Tracker
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 11: ") # Mementos
    # # ...
    # # ########################################################
    # logger.info("Response: reusablePlugs: data: plugs: 13: ") # Increase level
    # # ...

    # logger.info("-------\nInstanced Item (Class) 6917529901295685532")
    # logger.info("Response: sockets: data: sockets: ")
    # logger.info(manifest.get_inventory_item(1180408010))
    # logger.info(manifest.get_inventory_item(4188291233))
    # logger.info(manifest.get_inventory_item(11126525))
    # logger.info(manifest.get_inventory_item(40751621))
    # logger.info(manifest.get_inventory_item(1622227945))
    # logger.info(manifest.get_inventory_item(902052880))
    # logger.info("null")
    # logger.info("null")
    # logger.info("null")
    # logger.info("null")
    # logger.info(manifest.get_inventory_item(3303607908))
    # logger.info(manifest.get_inventory_item(2322202118))
    # logger.info(manifest.get_inventory_item(3727270518))
    # logger.info("Response: reusablePlugs: data: plugs: 4: ")
    # logger.info(manifest.get_inventory_item(4248210736))

if __name__ == "__main__":
    main()