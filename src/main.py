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
        format="%(asctime)s %(levelname)8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info("DIM Loadout Archiver")
    logger.debug("Verbose logging enabled")

    manifest = D2Manifest(Path.cwd() / "data/manifest.db")

    logger.info("Example DIM Loadout")
    logger.info("'S25 Solo GM Birthplace Healing'")
    logger.info("-----equipped:")
    logger.info(manifest.get_inventory_item(2357297366).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(859869931).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(1762785662).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(50291571).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(119228495).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(1011882337).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3663544278).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3685276035).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3941205951).get("displayProperties").get("name"))
    logger.info("-----item 3941205951 socket overrides:")
    logger.info(manifest.get_inventory_item(2979486801).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3686638442).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(2274196884).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(1470370538).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(1841016428).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(83039192).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(83039193).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(362132294).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(362132300).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(362132289).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(362132293).get("displayProperties").get("name"))
    # logger.info("-----mods:")
    # logger.info(manifest.get_inventory_item(1180408010).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(3832366019).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(3832366019).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(554409585).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(539459624).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(1180408010).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(1079896271).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(377010989).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(4287799666).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(3410844187).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(3410844187).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(3719981603).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(1180408010).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(4087056174).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(335129856).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(4087056174).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(1180408010).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(4188291233).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(11126525).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(40751621).get("displayProperties").get("name"))
    # logger.info(manifest.get_inventory_item(617569843).get("displayProperties").get("name"))
    logger.info("-----mods by bucket:")
    logger.info("-- " + manifest.get_inventory_bucket(14239492).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(965288073).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3975122240).get("displayProperties").get("name"))
    logger.info("-- " + manifest.get_inventory_bucket(20886954).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(965288073).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(2596599281).get("displayProperties").get("name"))
    logger.info("-- " + manifest.get_inventory_bucket(1585787867).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(965288073).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(3303607908).get("displayProperties").get("name"))
    logger.info("-- " + manifest.get_inventory_bucket(3448274439).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(965288073).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(702981643).get("displayProperties").get("name"))
    logger.info("-- " + manifest.get_inventory_bucket(3551918588).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(965288073).get("displayProperties").get("name"))
    logger.info(manifest.get_inventory_item(2179078680).get("displayProperties").get("name"))
    logger.info("-----inGameIdentifiers:")
    logger.info("https://bungie.net/" + manifest.get_loadout_color(3871954967).get("colorImagePath"))
    logger.info("https://bungie.net/" + manifest.get_loadout_icon(797343698).get("iconImagePath"))
    logger.info(manifest.get_loadout_name(2755629635).get("name"))


if __name__ == "__main__":
    main()