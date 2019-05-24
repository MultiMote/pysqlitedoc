#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ###################################################### #
# Author: MultiMote                                      #
# Description: pysqlitedoc dox generator                 #
# URL: https://github.com/MultiMote/pysqlitedoc          #
# ###################################################### #

import sqlite3
import json


db_path = "database.db"
dox_path = "input/database.dox"
comments_path = "table_comments.json"


db = sqlite3.connect(db_path)
output = open(dox_path, "w", encoding='utf-8')
comments = {}

try:
    json_file = open(comments_path, "r", encoding='utf-8')
    comments = json.load(json_file)
    json_file.close()
except Exception:
    pass

db.row_factory = sqlite3.Row

output.write("/*!\n")
output.write(" * \\page database_structure Database structure\n")

for tabledef in db.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite\\_%' ESCAPE '\\' ORDER BY name "):
    tablename = tabledef["name"]

    output.write(" *\n")
    output.write(" *\n")
    output.write(" * \\section db_table_{} \"{}\" table\n".format(tablename, tablename))

    try:
        output.write(" *\n")
        output.write(" * {}\n".format(comments.get(tablename).get("comment", "")))
        output.write(" *\n")
    except AttributeError:
        pass

    output.write(" * <table>\n")
    output.write(" * <tr>\n")
    output.write(" *  <th>Field</th>\n")
    output.write(" *  <th>Type</th>\n")
    output.write(" *  <th title=\"Primary key\">PK</th>\n")
    output.write(" *  <th title=\"Required (NOT NULL)\">NN</th>\n")
    output.write(" *  <th>Default</th>\n")
    output.write(" *  <th>Description</th>\n")
    output.write(" * </tr>\n")

    for field in db.execute("PRAGMA table_info({})".format(tablename)):
        output.write(" * <tr>\n")
        output.write(" *  <td>{}</td>\n".format(field["name"]))
        output.write(" *  <td>{}</td>\n".format(field["type"]))
        output.write(" *  <td style=\"text-align:center\">{}</td>\n".format("●" if field["pk"] == 1 else ""))
        output.write(" *  <td style=\"text-align:center\">{}</td>\n".format("●" if field["notnull"] == 1 else ""))
        output.write(" *  <td style=\"text-align:center\">{}</td>\n".format("`NULL`" if field["dflt_value"] is None else field["dflt_value"]))

        try:
            output.write(" *  <td>{}</td>\n".format(comments.get(tablename).get("fields").get(field["name"], "")))
        except AttributeError:
            output.write(" *  <td></td>\n")

        output.write(" * </tr>\n")

    output.write(" * </table>\n")

    foreign_keys = db.execute("PRAGMA foreign_key_list({})".format(tablename)).fetchall()

    if len(foreign_keys) > 0:
        output.write(" * <h2>\"{}\" foreign keys</h2>\n".format(tablename))
        output.write(" * <table>\n")
        output.write(" * <tr>\n")
        output.write(" *  <th>Local field</th>\n")
        output.write(" *  <th>Reference table</th>\n")
        output.write(" *  <th>Reference field</th>\n")
        output.write(" *  <th>On update</th>\n")
        output.write(" *  <th>On delete</th>\n")
        output.write(" * </tr>\n")
        for fkey in foreign_keys:
            output.write(" * <tr>\n")
            output.write(" *  <td>{}</td>\n".format(fkey["from"]))
            output.write(" *  <td>{}</td>\n".format(fkey["table"]))
            output.write(" *  <td>{}</td>\n".format(fkey["to"]))
            output.write(" *  <td>{}</td>\n".format(fkey["on_update"]))
            output.write(" *  <td>{}</td>\n".format(fkey["on_delete"]))
            output.write(" * </tr>\n")

        output.write(" * </table>\n")

output.write("*/\n")

output.close()
