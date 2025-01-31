#!/usr/bin/env python3

# File: run_query_w_date.py

"""
requires a parameter; the name of a file containing
a valid sql query with {today} place holders.
"""

import sys
from code.helpers import datestamp as today
from code.sql_code import fetch

query_file = sys.argv[1]
with open(sys.argv[1], 'r') as stream:
    query = stream.read().format(today=today)

print(today)
for line in fetch(query, from_file=False):
    print(line)


