#!/usr/bin/env python3

# File: code/helpers.py

import csv
import json
import datetime

today = datetime.datetime.today()
datestamp = today.strftime("%Y-%m-%d")

## Utility Functions:

def show_dict(mapping):
    for key, value in mapping.items():
        print(f"{key}: {value}", end = '; ')
    print()

def shortened_dict(mapping):
    """
    Returns the mapping with only keys that have values.
    !non string values may raise bugs ie int(0)!
    i.e. an integer value of zero would be removed.
    """
    return {key: value for key, value in mapping.items() if value}


def dump2json_file(data, json_file, verbose=True):
    """
    <json_file> if it exists will be overwritten!!
    """
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  json_file_obj.name))
        json.dump(data, json_file_obj)


def add2json_file(data, json_file, verbose=True):
    """
    <data> will be appended to <json_file> (which will be created
    if it doesn't already exist.
    """
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as j_file:
            if verbose:
                print('Loading existing (json) data from "{}".'
                        .format(j_file.name))
            data2add = json.load(j_file)
            if not isinstance(data2add, list):
                warning = [
                f"Warning: Content of {json_file} is not a list.",
                "Perhaps it was simply an empty file."
                "Beginning with an empty list",
                "Original content, if any, will be lost!"
                ]
                for line in warning: print(line)
                yn = input("Continue? (y/n) ")
                if yn and yn[0] in 'yY':
                    data2add = []
                else:
                    sys.exit()

        data2add.append(data)
    else:
        data2add = [data, ]
    with open(json_file, 'w', encoding='utf-8') as j_file:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  j_file.name))
        json.dump(data2add, j_file)


def get_json(file_name, report=None):
    """
    JSON reads 'file_name': clients expect a list of dicts.
    Provides optional reporting.
    """
    with open(file_name, 'r') as f_obj:
        add2report(report,
            f'Reading JSON file "{f_obj.name}".',
            also_print=True)
        return json.load(f_obj)


def dump2csv_file(listing, keys=None,
                         file_name="new_csv.csv"):
    """
    <listing> can be a list of iterables or a list of dicts
    in which case no need for the <keys> parameter.
    """
    if not len(listing) > 0:
        print("Nothing to store (code/helpers.dump2csv_file).")
        return
    with open(file_name, 'w', newline='') as outf:
        if isinstance(listing[0], dict):
            keys = [key for key in listing[0].keys()]
            writer = csv.DictWriter(outf, fieldnames=keys)
            writer.writeheader()
            for d in listing:
                writer.writerow(d)
        else:   # not dealing with a list of dicts!
            writer = csv.writer(outf)
            writer.writerow(keys)
            for iterable in listing:
                writer.writerow(iterable)

if __name__ == "__main__":
    print(datestamp)
