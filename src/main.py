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
    # =========== Args ===========
    parser = argparse.ArgumentParser(
        description="DIM Loadout Archiver"
    )
    # parser.add_argument("", help="", type=str)
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()

    # =========== Logging ===========
    log_level = logging.DEBUG if args.verbose else logging.INFO
    datefmt = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level = log_level,
        # format="%(asctime)s %(levelname)8s: %(message)s",
        format="\033[95m%(asctime)s %(levelname)8s:\033[0m\n %(message)s",
        # format="%(message)s",
        datefmt=datefmt
    )
    log_file_format = "%(asctime)s %(levelname)8s: %(message)s"
    # log_file_format = "\033[95m%(asctime)s %(levelname)8s:\033[0m\n %(message)s"
    # log_file_format = "%(message)s"

    log_file_handler = logging.FileHandler("output/output.log", mode="w")
    log_file_handler.setLevel(log_level)
    log_file_handler.setFormatter(logging.Formatter(log_file_format, datefmt=datefmt))
    
    # logger.addHandler(log_console_handler)
    logger.addHandler(log_file_handler)

    logger.info("DIM Loadout Archiver")
    logger.debug("Verbose logging enabled")

    # =========== Application ===========
    
    # TODO: Download the manifest locally instead
    manifest = D2Manifest(Path.cwd() / "data/manifest.db", verbose=args.verbose)

    bnet = DestinyAPI(manifest=manifest)
    bnet.authorize()

    with open("data/dim-api_loadouts_20250711-0854.json") as f: # DEBUG: Hard coded file name for now
        dim_loadouts = json.load(f)
        # logger.info(dim_loadouts) # DEBUG Full file
    
    for loadout in dim_loadouts["loadouts"]:
        # DEBUG look at a specific loadout
        # if loadout["id"] != "015918bc-a732-4c27-b8f2-54d708b67424":
        # if loadout["id"] != "016b1049-9650-436b-8624-bc6fad245911":
        # if loadout["id"] != "01c98aec-2173-404d-8094-dca10f0caa2b": 
        # if loadout["id"] != "7ffe28ce-c867-4481-9cf3-d87860d36d45": 
            # continue
            
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
                equipment = {}
                equipment["manifest_info"] = json.loads(manifest.get_inventory_item(equipped["hash"]))
                equipment["curated_roll"] = json.loads(manifest.get_curated_weapon(equipped["hash"]))
                equipment["instanced_roll"] = json.loads(bnet.get_instanced_item(equipped.get("id"), hash=equipped["hash"]))
                craftedDate = equipped.get("craftedDate")
                if craftedDate:
                    equipment["crafted_date"] = datetime.fromtimestamp(craftedDate).strftime("%Y-%m-%d %H:%M:%S UTC")
                logger.info(json.dumps(equipment, indent=2))

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
                equipment = {}
                equipment["manifest_info"] = json.loads(manifest.get_inventory_item(unequipped["hash"]))
                equipment["curated_roll"] = json.loads(manifest.get_curated_weapon(unequipped["hash"]))
                equipment["instanced_roll"] = json.loads(bnet.get_instanced_item(unequipped.get("id"), hash=unequipped["hash"]))
                craftedDate = unequipped.get("craftedDate")
                if craftedDate:
                    equipment["crafted_date"] = datetime.fromtimestamp(craftedDate).strftime("%Y-%m-%d %H:%M:%S UTC")
                logger.info(json.dumps(equipment, indent=2))
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

        logger.info(f"\n-------------------------------------------\n-----end of loadout: {loadout['id']} {loadout['name']}\n")

        # break # DEBUG just running the first found loadout for now


if __name__ == "__main__":
    main()