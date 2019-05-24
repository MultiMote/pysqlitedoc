#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ###################################################### #
# Author: MultiMote                                      #
# Description: pysqlitedoc table_comments.json generator #
# URL: https://github.com/MultiMote/pysqlitedoc          #
# ###################################################### #

import sqlite3
import json

db_path = "database.db"
comments_path = "table_comments.json"


db = sqlite3.connect(db_path)
json_data = {}

try:
    json_file = open(comments_path, "r", encoding='utf-8')
    json_data = json.load(json_file)
    json_file.close()
except Exception:
    pass

db.row_factory = sqlite3.Row

for tabledef in db.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite\\_%' ESCAPE '\\' "):
    tablename = tabledef["name"]

    if json_data.get(tablename) is None:
        json_data[tablename] = {}

    if json_data.get(tablename).get("comment") is None:
        json_data[tablename]["comment"] = ""

    if json_data.get(tablename).get("fields") is None:
        json_data[tablename]["fields"] = {}

    for field in db.execute("PRAGMA table_info({})".format(tablename)):
        if json_data.get(tablename).get("fields").get(field["name"]) is None:
            json_data[tablename]["fields"][field["name"]] = ""

json_file = open(comments_path, "w", encoding='utf-8')
json.dump(json_data, json_file, indent=4)
json_file.close()
