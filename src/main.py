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
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info("DIM Loadout Archiver")
    logger.debug("Verbose logging enabled")

    bnet = DestinyAPI()
    bnet.authorize()
    r = bnet.get_instanced_item(6917530072480039762)
    logger.info(f"result: {r.get('Message')}")
    logger.info(json.dumps(r))



    # TODO: Download the manifest locally instead
    # manifest = D2Manifest(Path.cwd() / "data/manifest.db", verbose=True)

    # # https://github.com/DestinyItemManager/dim-api/blob/master/api/shapes/loadouts.ts
    # logger.info("Example DIM Loadout")
    # logger.info("'S25 Solo GM Birthplace Healing'")
    # logger.info("\n\n\n-------------------------------------------\n-----equipped:\n\n\n")
    # logger.info(manifest.get_inventory_item(2357297366)) # Witherhoard Exotic Primary
    # logger.info(manifest.get_inventory_item(859869931)) # Nullify Legendary Energy
    # logger.info(manifest.get_inventory_item(1762785662)) # VS Chill Inhibitor Legendary Power
    # logger.info(manifest.get_inventory_item(50291571)) # Speaker's Sight
    # logger.info(manifest.get_inventory_item(119228495))
    # logger.info(manifest.get_inventory_item(1011882337))
    # logger.info(manifest.get_inventory_item(3663544278))
    # logger.info(manifest.get_inventory_item(3685276035))
    # logger.info(manifest.get_inventory_item(3941205951)) # Dawnblade Subclass
    # logger.info("\n\n\n-------------------------------------------\n-----item 3941205951 socket overrides:\n\n\n")
    # logger.info(manifest.get_inventory_item(2979486801))
    # logger.info(manifest.get_inventory_item(3686638442))
    # logger.info(manifest.get_inventory_item(2274196884))
    # logger.info(manifest.get_inventory_item(1470370538))
    # logger.info(manifest.get_inventory_item(1841016428))
    # logger.info(manifest.get_inventory_item(83039192))
    # logger.info(manifest.get_inventory_item(83039193))
    # logger.info(manifest.get_inventory_item(362132294))
    # logger.info(manifest.get_inventory_item(362132300))
    # logger.info(manifest.get_inventory_item(362132289))
    # logger.info(manifest.get_inventory_item(362132293))
    # logger.info("\n\n\n-------------------------------------------\n-----unequipped:\n\n\n")
    # # logger.info("-----mods:")
    # # logger.info(manifest.get_inventory_item(1180408010))
    # # logger.info(manifest.get_inventory_item(3832366019))
    # # logger.info(manifest.get_inventory_item(3832366019))
    # # logger.info(manifest.get_inventory_item(554409585))
    # # logger.info(manifest.get_inventory_item(539459624))
    # # logger.info(manifest.get_inventory_item(1180408010))
    # # logger.info(manifest.get_inventory_item(1079896271))
    # # logger.info(manifest.get_inventory_item(377010989))
    # # logger.info(manifest.get_inventory_item(4287799666))
    # # logger.info(manifest.get_inventory_item(3410844187))
    # # logger.info(manifest.get_inventory_item(3410844187))
    # # logger.info(manifest.get_inventory_item(3719981603))
    # # logger.info(manifest.get_inventory_item(1180408010))
    # # logger.info(manifest.get_inventory_item(4087056174))
    # # logger.info(manifest.get_inventory_item(335129856))
    # # logger.info(manifest.get_inventory_item(4087056174))
    # # logger.info(manifest.get_inventory_item(1180408010))
    # # logger.info(manifest.get_inventory_item(4188291233))
    # # logger.info(manifest.get_inventory_item(11126525))
    # # logger.info(manifest.get_inventory_item(40751621))
    # # logger.info(manifest.get_inventory_item(617569843))
    # logger.info("\n\n\n-------------------------------------------\n-----mods by bucket:\n\n\n")
    # logger.info(f"-- {format(manifest.get_inventory_bucket(14239492))}")
    # logger.info(manifest.get_inventory_item(965288073))
    # logger.info(manifest.get_inventory_item(3975122240))
    # logger.info(f"-- {format(manifest.get_inventory_bucket(20886954))}")
    # logger.info(manifest.get_inventory_item(965288073))
    # logger.info(manifest.get_inventory_item(2596599281))
    # logger.info(f"-- {format(manifest.get_inventory_bucket(1585787867))}")
    # logger.info(manifest.get_inventory_item(965288073))
    # logger.info(manifest.get_inventory_item(3303607908))
    # logger.info(f"-- {format(manifest.get_inventory_bucket(3448274439))}")
    # logger.info(manifest.get_inventory_item(965288073))
    # logger.info(manifest.get_inventory_item(702981643))
    # logger.info(f"-- {format(manifest.get_inventory_bucket(3551918588))}")
    # logger.info(manifest.get_inventory_item(965288073))
    # logger.info(manifest.get_inventory_item(2179078680))
    # logger.info("\n\n\n-------------------------------------------\n-----inGameIdentifiers:\n\n\n")
    # logger.info("https://bungie.net/" + manifest.get_loadout_color(3871954967).get("colorImagePath"))
    # logger.info("https://bungie.net/" + manifest.get_loadout_icon(797343698).get("iconImagePath"))
    # logger.info(manifest.get_loadout_name(2755629635).get("name"))
    # logger.info("\n\n\n-------------------------------------------\n-----artifactUnlocks:\n\n\n")
    # logger.info(manifest.get_inventory_item(4152932100))
    # logger.info(manifest.get_inventory_item(4152932103))
    # logger.info(manifest.get_inventory_item(4152932097))
    # logger.info(manifest.get_inventory_item(2317325398))
    # logger.info(manifest.get_inventory_item(2317325399))
    # logger.info(manifest.get_inventory_item(2317325393))
    # logger.info(manifest.get_inventory_item(3547711350))
    # logger.info(manifest.get_inventory_item(3547711348))
    # logger.info(manifest.get_inventory_item(3547711346))
    # logger.info(manifest.get_inventory_item(51032917))
    # logger.info(manifest.get_inventory_item(1328115226))
    # logger.info(manifest.get_inventory_item(1328115229))


if __name__ == "__main__":
    main()