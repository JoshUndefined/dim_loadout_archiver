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
    # print(manifest.get_inventory_item_definition(1762785662))
    print(manifest.get_inventory_item_definition(1762785662).get("displayProperties"))

if __name__ == "__main__":
    main()