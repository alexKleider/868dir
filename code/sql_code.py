#!/usr/bin/env python3

# File: code/sql_code.py

import csv
import sqlite3

db_file = "Secret/868.db"

def initDB(path=db_file):
    """
    Returns a connection ("db")
    and a cursor ("clubcursor")
    """
    try:
        db = sqlite3.connect(path)
        clubcursor = db.cursor()
    except sqlite3.OperationalError:
        print("Failed to connect to database:", path)
        db, clubcursor = None, None
        raise
    return db, clubcursor


def closeDB(database, cursor):
    try:
       cursor.close()
       database.commit()
       database.close()
    except sqlite3.OperationalError:
       print( "problem closing database..." )
       raise


def fetch(sql_source, db=db_file, params=None, data=None,
                    from_file=True, commit=False,
                    verbose=False):
    """
    <sql_source> must be a string: either the name of a file
    containing a valid sqlite3 query or (if <from_file> is set
    to False) the query itself. The query is executed on the <db>.
    Only one (if any) of the following should be provided:
        <params> must be an iterable of length to match number
            of qmark placeholders in the query. Remember to use
            the '%' character as a suffix (or prefix or both.)
        <data> must be a dict with all keys necessary to match
            all place holders in the query. Remember place holder
            names are prefaced by a colon in the query.
            eg: (:key1, :key2).
    Be aware that the query might return an empty list.
    """
    if from_file:
        with open(sql_source, 'r') as source:
            query = source.read()
#       _ = input(f"### Query begins next line\n{query}")
    else: query = sql_source
    if verbose:
        print("Query being called is...")
        _ = input(query)
    db, cur = initDB(db)
    if data:
        if verbose:
            _ = input(f"data: {data}")
#       cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)
        cur.executemany(query, data)
    elif params:
#       _ = input(f"params set to '{params}'")
        cur.execute(query, params)
    else:
        cur.execute(query)
#   _ = input(
#       f"get_query_result returning the following:\n {ret}")
    ret = cur.fetchall()
    if commit:
        db.commit()
        if verbose:
            _ = input("Committed!")
    closeDB(db, cur)
    if verbose:
        print(f"routines.fetch returning {ret}")
    return ret


def dicts_from_query(query, keys):
    """
    Yields dicts.
    """
    res = fetch(query, from_file=False)
    for entry in res:
        d = dict(zip(keys, entry))
        yield d

def query2csv(query, keys, fname):
    with open(fname, 'w', newline='') as stream:
        dictwriter = csv.DictWriter(stream, keys)
        dictwriter.writeheader()
        for mapping in dicts_from_query(query, keys):
            dictwriter.writerow(mapping)


def experiment0():
    print("Running experiment 0")
    db = sqlite3.connect(db_file)
    cur = db.cursor()
    res = cur.execute("""SELECT * FROM people""")
#   ret = res.fetchall()
    for item in res:
        print(item)

def experiment1():
    print("Running experiment 1")
    res = fetch("""SELECT * FROM people
                ORDER BY last, first, id""",
                from_file=False)
    for listing in res:
        print(listing)


def experiment2():
    outfile = "868Directory.csv"
    print("Running experiment 2")
    keys = (
        "id",
        "entry_date",
        "first",
        "mi",
        "last",
        "suffix",
        "phone",
        "address",
        "town",
        "state",
        "country",
        "email",
        )
    keys = keys[2:]
    key_listing = ', '.join(keys)
    query2csv(f"""SELECT {key_listing} FROM people
              ORDER BY last, first""",
                keys, outfile)
    print(f"check file: {outfile}.")


if __name__ == "__main__":
    experiment2()
