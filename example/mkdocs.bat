@echo off
python ..\mksqlitedoc_json.py && python ..\mksqlitedoc.py && doxygen