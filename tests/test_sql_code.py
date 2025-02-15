#!/usr/bin/env python3

# File: tests/test_sql_code.py

"""
listings = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", listings)
con.commit()

SQL operations usually need to use values from Python variables. However,
beware of using Python’s string operations to assemble queries, as they
are vulnerable to SQL injection attacks. For example, an attacker can
simply close the single quote and inject OR TRUE to select all rows:
    
Instead, use the DB-API’s parameter substitution. To insert a variable
into a query string, use a placeholder in the string, and substitute the
actual values into the query by providing them as a tuple of values to
the second argument of the cursor’s execute() method.


An SQL statement may use one of two kinds of placeholders: question marks
(qmark style) or named placeholders (named style). For the qmark style,
parameters must be a sequence whose length must match the number of
placeholders, or a ProgrammingError is raised. For the named style,
parameters must be an instance of a dict (or a subclass), which must
contain keys for all named parameters; any extra items are ignored. 

qmark style: iterable of values maching number of "?" marks
If more than one entry: use executemany with a list of iterables.
named style: use ?keyname as place holders and a dict as 2nd param.
If more than one: use executemany with a list of dicts
"""

import sys
import os
import pytest
sys.path.insert(0, os.path.split(sys.path[0])[0])
import sqlite3
from src import sql_code

exclude = """
def test_initDB():
    db, cur = src.initDB(path=":memory:")
    assert (db, cur) == ("db", "cur")
"""

@pytest.fixture
def setup_database():
    """ Fixture to set up the in-memory database with test data """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT DEFAULT "",
            first TEXT DEFAULT "",
            mi TEXT DEFAULT "",
            last TEXT DEFAULT "",
            suffix TEXT DEFAULT "",
            phone TEXT DEFAULT "",
            address TEXT DEFAULT "",
            town TEXT DEFAULT "",
            state TEXT DEFAULT "",
            postal_code TEXT DEFAULT "",
            country TEXT DEFAULT "",
            email TEXT DEFAULT ""
        )''')
    sample_data = [
        ("2025-01-05", "Joe", "Shmo", "602/392-4525", "23 Any St",
         "Sometown", "AZ", "85321", "USA", "joeshmo@provider.com"),
        ("2025-01-06", "George", "Smith", "251/530-2272", "67 Long Rd",
         "Anytown", "AL", "36608", "USA", "joeshmo@provider.com"),
        ("2025-01-07", "Andy", "Curtis", "231/392-2545", "PO Box 8452",
         "Georgetown", "MI", "49123", "USA", "joeshmo@provider.com"),
        ("2025-01-08", "Bob", "Jones", "515/391-6309", "824 A St",
         "Pheniz", "IA", "52800", "USA", "joeshmo@provider.com"),
        ("2025-01-09", "Sharon", "Sinclair", "986/297-7461", "4523 Hwy 9",
         "Backwater", "ID", "83298", "USA", "joeshmo@provider.com"),
        ("2025-01-10", "Billy", "Bagins", "808/333-6702", "RR#52",
         "Evansville", "HI", "96750", "USA", "joeshmo@provider.com"),
    ]

    cursor.executemany('''
        INSERT INTO people (
            entry_date, first, last, phone, address, town, state,
            postal_code, country, email)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       sample_data)
    yield conn


def test_connection(setup_database):
    # Test to make sure that there are 2 items in the database

    cursor = setup_database
    assert len(list(cursor.execute('SELECT * FROM people'))) == 6

