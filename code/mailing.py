#!/usr/bin/env python3

# File: code/mailing.py
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

import json
import sql_code
import helpers

today = helpers.datestamp

query = f"""
    SELECT P.id, PS.statusID,
        P.first, P.mi, P.last, P.suffix, P.phone, P.address,
        P.town, P.state, P.postal_code, P.country, P.email
    FROM people AS P
    JOIN person_status AS PS
        ON P.id = PS.personID
        AND PS.begin <= "{today}"
        AND (PS.end = "" OR PS.end > "{today}")
        ;
        """
keys = ("P.id, PS.statusID, " +
        "P.first, P.mi, P.last, P.suffix, P.phone, P.address, "
        + "P.town, P.state, P.postal_code, P.country, P.email")
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

    "Bolinas", "CA", "94924", "USA" will be assumed where
blank entries occur for town, state, postal_code and country.

    Please check whether or not your email is being displayed
and let it be known if you'd like that changed.

Sincerely,
868Directory
"""

emails = [ ]
email_file = "Secret/emails.json"

def emails2file(emails, file_name=email_file):
    if emails:
        helpers.dump2json_file(emails,
                email_file)
        n = len(emails)
        efile = email_file
        print(f"{n} emails sent to {efile}.")
        print(f"Emails ({len(holder.emails)} in " +
            f"number) sent to {email_file}")
    else:
        print("No emails to send.")


def select_status():
    """
    1:active, 2:inactive, 3:no-email
    """
    pass

def dump2json_file(data, json_file, verbose=True):
    """
    <json_file> if it exists will be overwritten!!
    """
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  json_file_obj.name))
        json.dump(data, json_file_obj)

def t1():
    _ = input(f'Query: """{query}""" ')
    res = sql_code.fetch(query, from_file=False)
    print(keys)
    for line in res:
        print(line)
    _ = input()
    print(body.format(name=name, entry=entry))

def t2():
    yn = input(f"Subject set to <{subject}>. Continue? (y/n) ")
    if yn and yn[0] in "nN":
        return
    res = sql_code.fetch(query, from_file=False)
    for line in res:
        print(line)
        email_address = line[-1]
        name = f"{line[2]} {line[4]}:"
        if int(line[1]) == 3:
            line = [item for item in line]
            line[-1] = ''
        letter_body = body.format(name=name, entry=line[2:])
        print(letter_body)
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
    dump2json_file(emails, email_file, verbose=True)

if __name__ == "__main__":
    t2()


