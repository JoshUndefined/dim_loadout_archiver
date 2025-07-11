# Helper class to get data from D2 manifest

import json
import sqlite3
from pathlib import Path

class D2Manifest:
    def __init__(self, manifest_path):
        self._manifest_path = manifest_path
        conn = sqlite3.connect(manifest_path)
        self._cur = conn.cursor()

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

    def get_inventory_item_definition(self, hash):
        return self.get_definition("DestinyInventoryItemDefinition", hash)

    def get_inventory_bucket_definition(self, hash):
        return self.get_definition("DestinyInventoryBucketDefinition", hash)

    def get_loadout_color_definition(self, hash):
        return self.get_definition("DestinyLoadoutColorDefinition", hash)

    def get_loadout_icon_definition(self, hash):
        return self.get_definition("DestinyLoadoutIconDefinition", hash)

    def get_loadout_name_definition(self, hash):
        return self.get_definition("DestinyLoadoutNameDefinition", hash)

    # SQlite3 IDs are Signed Int, D2 Hash are Unsigned Int
    def _d2_hash(self, hash):
        return hash - 2**32 if hash > 0x7FFFFFFF else hash