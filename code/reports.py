#!/usr/bin/env python3

# File: code/reports.py

import helpers
import sql_code

today = helpers.datestamp
keys = ("id,entry_date,first,mi,last,suffix,phone,"
    +"address,town,state,postal_code,country,email")
keys = keys.split(",")
selections = ", ".join(["P."+key for key in keys])
keys_w_status = [key for key in keys]
keys_w_status.append("S.status")
selections_w_status = selections + ", S.status"

query = f"""
    /* Sql/active.sql */
    /* formatting required */
    SELECT
    {selections}
    FROM people as P
    JOIN person_status as PS
    ON P.id = PS.personID
    WHERE PS.statusID = 1
    AND PS.begin < "{today}"
    AND (PS.end = "" OR PS.end > "{today}")
    ; """

query1 = f"""
    /* Sql/active.sql */
    /* "{today}" needs to be formatted */
    SELECT {selections_w_status} FROM people as P
    JOIN person_status as PS
    ON P.id = PS.personID
    JOIN stati as S
    ON S.id = PS.statusID
    WHERE
--  PS.statusID = 1 AND
    PS.begin < "{today}"
    AND (PS.end = "" OR PS.end > "{today}")
    ; """


def line2dict(iterable, keys):
    return {key: value for key, value in zip(keys, iterable)}

def report():
    #res = sql_code.fetch(query, from_file=False)
    #helpers.dump2csv_file(res,
    #            keys=keys,
    #            file_name="active.csv")
    _ = input(query1)
    res = sql_code.fetch(query1, from_file=False)
    for line in res:
        d = line2dict(line, keys_w_status)
        for key, value in d.items():
            print(f"{key}: {value}")
#       _ = input()



