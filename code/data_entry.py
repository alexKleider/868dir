#!/usr/bin/env python3

# File: ~/Projects/868dir/code/data_entry.py

import gui
import sql_code
import helpers

people_keys = ("id, entry_date, first, mi, last, suffix, phone, " +
                "address, town, state, postal_code, country, email")
people_keys = people_keys.split(', ')

def insert_into(table_name, mapping):
    keys = mapping.keys()
    keys = ", ".join(keys)
    values = [f'"{value}"' for value in mapping.values()]
    values = ", ".join(keys)
    query = f"""
        INSERT INTO {table_name}
        ({keys})
        VALUES
        ({values})
        ; """
    _ = input(query)


def add2people():
    mapping = {key:"" for key in people_keys[2:]}
#   print(mapping)
    new_mapping = helpers.shortened_dict(
            gui.change_mapping(mapping))
#   print(new_mapping)
    new_mapping["entry_date"] = helpers.datestamp
    keys = new_mapping.keys()
    values = ", ".join(
        [f'"{value}"' for value in new_mapping.values()])
    query = f"""INSERT INTO people
        ({", ".join(keys)})
        VALUES ({values})
        ; """
#   _ = input(query)
    if gui.yes_no(query, title="Execute?"):
        sql_code.fetch(query, from_file=False,
                  commit=True, verbose=False)
    if gui.yes_no("Activate person just entered?",
                                title="Yes or No"):
        personID, first, last = sql_code.fetch(
            """SELECT id, first, last FROM people
            ORDER BY id DESC LIMIT 1;""",   # last entry
            from_file=False)[0]
#       _ = input(f"{personID:>3}  {first}  {last}")
        query = f""" INSERT INTO person_status
                (personID, statusID, begin) 
            VALUES ({personID}, 1, "{helpers.datestamp}");"""
        if gui.yes_no(query, title="Execute?"):
            sql_code.fetch(query, from_file=False,
                           commit=True)
# Still need to make an entry in the person_status table!!
    pass

if __name__ == "__main__":
    add2people()

