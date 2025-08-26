import sys
import logging
logger = logging.getLogger(__name__)
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from lib.d2manifest import D2Manifest

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
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info("DIM Loadout Archiver")
    logger.debug("Verbose logging enabled")


    # TODO: Download the manifest locally instead
    manifest = D2Manifest(Path.cwd() / "data/manifest.db", verbose=True)


    with open("data/dim-api_loadouts_20250711-0854.json") as f: # DEBUG: Hard coded file name for now
        dim_loadouts = json.load(f)
        # logger.info(dim_loadouts)
    
    # print(dim_loadouts["sync"])
    # print(dim_loadouts["loadouts"])
    # print(dim_loadouts["syncToken"])
    
    for loadout in dim_loadouts["loadouts"]:
        # # DEBUG look at a specific loadout
        # if loadout["id"] != "015918bc-a732-4c27-b8f2-54d708b67424":
        #     continue
            
        logger.info(f"-------------------------------------------\nLoadout {loadout['id']} {loadout['name']}")
        # logger.info(loadout) # DEBUG https://github.com/DestinyItemManager/dim-api/blob/master/api/shapes/loadouts.ts

        logger.info("\n-------------------------------------------\n-----info:\n")
        logger.info(f"DIM id: {loadout['id']}")
        logger.info(f"name: {loadout['name']}")
        logger.info(f"classType: {loadout['classType']}")
        logger.info(f"createdAt: {loadout['createdAt']}")
        logger.info(f"lastUpdatedAt: {loadout['lastUpdatedAt']}")
        logger.info(f"notes: {loadout['notes']}")
        if "inGameIdentifiers" in loadout["parameters"].keys():
            inGameIdentifier = loadout["parameters"]["inGameIdentifiers"]
            logger.info("inGameLoadoutColor: https://bungie.net/" + manifest.get_loadout_color(inGameIdentifier["colorHash"]).get("colorImagePath"))
            logger.info("inGameLoadoutIcon: https://bungie.net/" + manifest.get_loadout_icon(inGameIdentifier["iconHash"]).get("iconImagePath"))
            logger.info("inGameLoadoutName: " + manifest.get_loadout_name(inGameIdentifier["nameHash"]).get("name"))
    
        logger.info("\n-------------------------------------------\n-----equipped:\n")
        for equipped in loadout["equipped"]:
            logger.info(manifest.get_inventory_item(equipped["hash"]))

            if "socketOverrides" in equipped.keys():
            # Subclass selectable details like Super, Aspects, Abilities
                logger.info("\n-------------------------------------------\n-----socketOverrides:\n")
                for subclass in equipped["socketOverrides"].values():
                    logger.info(manifest.get_inventory_item(subclass))

        logger.info("\n-------------------------------------------\n-----unequipped:\n")
        for unequipped in loadout["unequipped"]:
            logger.info(manifest.get_inventory_item(unequipped["hash"]))

        logger.info("\n-------------------------------------------\n-----mods:\n")
        # These are "loose" armor mods set in DIM that the DIM loadout generator will assign to armor
        for mod in loadout["parameters"]["mods"]:
            logger.info(manifest.get_inventory_item(mod))

        logger.info("\n-------------------------------------------\n-----mods by bucket:\n")
        # Cosmetic armor mods by armor slot
        for inventoryBucket in loadout["parameters"]["modsByBucket"]:
            logger.info(f"-- Bucket: {manifest.get_inventory_bucket(int(inventoryBucket))}")
            for mod in loadout["parameters"]["modsByBucket"][inventoryBucket]:
                # logger.info(mod)
                logger.info(manifest.get_inventory_item(mod))

        if "artifactUnlocks" in loadout["parameters"].keys():
            logger.info("\n-------------------------------------------\n-----artifactUnlocks:\n")
            # Seasonal artifact mods
            for artifactMod in loadout["parameters"]["artifactUnlocks"]["unlockedItemHashes"]:
                # logger.info(artifactMod)
                logger.info(manifest.get_inventory_item(artifactMod))



        break # DEBUG just running the first found loadout for now


if __name__ == "__main__":
    main()