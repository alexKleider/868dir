#!/usr/bin/env python3

# File: code/menu.py
#  was initially called mailing.py
"""
email = {     # email format...
    'From': sender,       # Mandatory field.
#   'Sender': sender,     # 0 or 1
#   'Reply-To': sender,   # 0 or 1
    'To': recipients,  # 1 or more, ',' separated
    'Cc': '',             # O or more comma separated
    'Bcc': '',            # O or more comma separated
    'Subject': subject,   # 0 or 1
    'attachments': [],
    'body': body,
}
"""

import csv
import json
import sql_code
import helpers
import gui
import data_entry

today = helpers.datestamp

csv_file_name = f"Secret/{today}.csv"
json_file_name = f"Secret/{today}.json"
email_file_name = f"Secret/{today}-emails.json"

query = f"""  /* also found in sql/venkat.sql */
    SELECT P.id, S.status,
        P.first, P.mi, P.last, P.suffix, P.phone, P.address,
        P.town, P.state, P.postal_code, P.country, P.email
    FROM people AS P
    JOIN stati as S
        ON PS.statusID = S.id
    JOIN person_status AS PS
        ON P.id = PS.personID
        AND PS.begin <= "{today}"
        AND (PS.end = "" OR PS.end > "{today}")
        ;
        """
# Use ''.join(list_of_strings) instead of += for building large strings
keys = ''.join((
        "P.id, ",
        "PS.status, ",
        "P.first, P.mi, P.last, P.suffix, P.phone, P.address, ",
        "P.town, P.state, P.postal_code, P.country, P.email"))
keys = [part.split(".")[1] for part in keys.split(", ")]

mappings = sql_code.dicts_from_query(query, keys)

print("running code/mailing.py")

sender = "868directory@gmail.com"
recipients = ""
subject = "Data verification"
entry = "First,MI,Last,JR,0868,PO Box 999,,,,,me@provider.net"
name = "NAME"
body = f"""
Dear {{name}}:
    This is to acknowledge that we've got you in our database.

    Also, it gives you an opportunity to check that the data to
be presented is as you want it.  Available keys and what is
planned for "your" entry are as follows:
    {",".join(keys[2:])}
    {{entry}}

    Only the last four digits of 415/868 phone numbers will
be listed.  More than one phone number may be provided.
Let it be known if you'd like a number to be specified as that
of a cell/mobile phone.

    "Bolinas", "CA", "94924", "USA" will be assumed where
blank entries occur for town, state, postal_code and country.

    Please check whether or not your email is being displayed
and let it be known if you'd like that changed.

Sincerely,
868Directory
"""

emails = [ ]

def emails2file(emails, file_name=email_file_name):
    if emails:
        helpers.dump2json_file(emails,
                file_name)
        n = len(emails)
        print(f"{n} emails sent to {file_name}.")
        print(
            f"Emails ({n} in number) sent to {email_file}")
    else:
        print("No emails to send.")


def select_status():
    """
    1:active, 2:inactive, 3:no-email
    """
    pass

def create_csv():
    res = sql_code.fetch(query, from_file=False)
    with open(csv_file_name, 'w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(keys)
#       print(keys)
        for line in res[1:]:
            writer.writerow(line)
#           print(line)
        print(f"Created '{stream.name}'.")
        pass

def create_json():
    res = sql_code.fetch(query, from_file=False)
    jdata = [{key: value for (key, value) in zip(keys, values)} for
             values in res]
#   for mapping in jdata:
#       print(mapping)
    helpers.dump2json_file(jdata, json_file_name)
    print(f"Created '{json_file_name}'.")


def mailing():
    
    ids2include = [30, 31 ]
#   ids2include = None

    yn = input(f"Subject set to <{subject}> and\n"+ 
       f"recipient IDs are {ids2include}. Continue? (y/n) ")
    if yn and yn[0] in "nN":
        return
#   _ = input(query)
    res = sql_code.fetch(query, from_file=False)
    for line in res:
#       print(line)
        personID = line[0]
        if ids2include and not (personID in ids2include):
            continue
            emails.append(e_rec)
        email_address = line[-1]
        name = f"{line[2]} {line[4]}:"
        if line[1] == "no-email":
            line = [item for item in line]
            line[-1] = ''
        letter_body = body.format(name=name, entry=line[2:])
#       print(letter_body)
        e_rec = {     # email format...
            'From': sender,
            'Reply-To': sender,
            'To': email_address,
#           'Cc': '',
            'Bcc': '868directory@gmail.com',
            'Subject': subject,
#           'attachments': [],
            'body': letter_body,
        }
#       yn = input("continue? y/n: ")
#       if yn and yn[0] in "Nn":
#           break
        emails.append(e_rec)
    helpers.dump2json_file(emails, email_file_name, verbose=True)


def main():
    carte = dict(
        add_entry= data_entry.add2people,
        mailing= mailing,
        csv= create_csv,
        json= create_json,
        )
    func = gui.pick_func(carte)
    if func:
#       _ = input(f"func: {func.__name__}")
        func()
    else:
        print("Menu aborted!")

if __name__ == "__main__":
    main()
#   mailing()
#   create_csv()
#   create_json()

