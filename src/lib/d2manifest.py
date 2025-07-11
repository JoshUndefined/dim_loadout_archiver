# Helper class to get data from D2 manifest

import json
import sqlite3
from pathlib import Path

class D2Manifest:
    def __init__(self, manifest_path):
        self._manifest_path = manifest_path
        conn = sqlite3.connect(manifest_path)
        self._cur = conn.cursor()

    def get_inventory_item_definition(self, hash):
        self._cur.execute(
            "SELECT json FROM DestinyInventoryItemDefinition WHERE id = ?",
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

    # SQlite3 IDs are Signed Int, D2 Hash are Unsigned Int
    def _d2_hash(self, hash):
        return hash - 2**32 if hash > 0x7FFFFFFF else hash