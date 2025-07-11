import sys
import logging
logger = logging.getLogger(__name__)
import argparse
import json
import sqlite3
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument("", help="", type=str)
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()

    logging.basicConfig(
        level = logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.debug("Verbose logging enabled")
    logger.info("")

if __name__ == "__main__":
    main()