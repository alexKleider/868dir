#!/usr/bin/env python3

# File: display_emails.py

"""
Usage:
    $ ./display_emails.py [outfile]

If not specified, <outfile> defaults to "emails.txt".
"""

import sys
import json
from src import helpers

today = helpers.datestamp
default_in_file = f"Secret/{today}-emails.json"
default_out_file = f'{today}-emails.txt'

if len(sys.argv) > 1:
    outf = sys.argv[1]
else:
    outf = default_out_file

print(f"Using {default_in_file} as default  input file...")
inf = input(f"<Enter> to accept or enter an alternative: ")
if inf: default_in_file = inf


def get_json(file_name):
    """
    JSON reads 'file_name': clients expect a list of dicts.
    """
    with open(file_name, 'r') as f_obj:
        return json.load(f_obj)

def display_emails(infile=default_in_file):
    records = get_json(infile)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
#           _ = input("{}: {}".format(field, record[field]))
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)

if __name__ == '__main__':
    with open(outf, 'w') as stream:
        print(f"Opening file '{stream.name}'...")
        stream.write(display_emails())
    print(f"Ouput written to {outf}")

