#!/usr/bin/env python3

# File: Projects/868dir/code/gui.py

"""
Collecting what's useful in Git/Sql/Code/textual.py and refining it
"""

import PySimpleGUI as sg
import helpers
import sql_code

font_index = 2  # adjust for readability

fonts = (          #  vv -- size parameter
        ("Helvetica", 10),  # the default
        ("Helvetica", 15),
        ("Helvetica", 20),
        ("Helvetica", 25),
        )
font= fonts[font_index]
    # Above code only to adjust size for readability
    #making text large enough to read.  Default size is 10.

def yes_no(question, title="Run query?", font=font):
    return sg.popup_yes_no(question,
            title=title, font=font) == "Yes"


def get_fields(fields, header="Enter values for each key",
               font=font):
    """
    Prompts user to supply values for each field.
    Returns None if user aborts, otherwise...
    Returns a dict keyed by <fields>,
    values are the entered (possibly empty) strings
    # Has been tested.
    """
    layout = [[sg.Text(header)],]
    layout.extend([
        [sg.Text(field), 
            sg.Input(expand_x=True, key=field)]
        for field in fields
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window('Enter values', layout, font=font)
#   event, values = window.read()
    event, the_dict = window.read()
    window.close()
    if event in (None, "Cancel"):
        return
    return the_dict

def change_mapping(mapping,
            headers=["Correct or Enter new value(s)",
                    "Choose from...",],
            font=font):
    """
    Prompts user to change/enter mapping values.
    Returns a new/modified dict or None if user aborts.
    <mapping> remains unchanged.
    """
    layout = [[sg.Text(headers[0])],]
    layout.extend([
        [sg.Text(key), 
            sg.Input(expand_x=True, key=key, default_text=value)]
        for key, value in mapping.items()
            ])
    layout.append([sg.Button('OK'), sg.Button('Cancel')])

    window = sg.Window(headers[1], layout,font=font)
    event, new_dict = window.read()
    window.close()
    if event in (None, "Cancel"):
        return
    return new_dict


def pick(query, keys, format_string,
            header="CHOOSE ONE",
            subheader="Choices are..."):
    """
    Uses <query> to collect a list of dicts and presents
    user with a corresponding list of choices, each a
    <format_string> formatted using the query results.
    Length of each query result line must == len(keys)
    Returns chosen dict or None (if none available or
    user aborts/cancels.)
    """
    res = sql_code.fetch(query, from_file=False)
    l = len(res)
    if not l:
        print("Empty query result...")
        return
    l = len(res[0])
    if l != len(keys):
        print("length mismatch: keys and query result")
        return
    mappings = []
    for line in res:
        mappings.append({key: value for key, value in zip(
            keys, line)})
    if not mappings:
        print("No records provided ==> exit")
        return
    options = [format_string.format(**rec)
            for rec in mappings]
    listing = zip(range(len(options)), options)
    for_display = [f"{item[0]:>2}: {item[1]}"
                for item in listing]
    layout=[[sg.Text(subheader,size=(50,1),
#           font='Lucida',justification='left'
            )],
            [sg.Listbox(values=for_display,
                select_mode='extended',
                key='CHOICE', size=(50,len(mappings)))],
            [sg.Button('SELECT',
#               font=('Times New Roman',12)
                ),
            sg.Button('CANCEL',
#                   font=('Times New Roman',12)
                    )
            ]]
    win =sg.Window(header,layout)
    e, v = win.read()
    win.close()
    if not v["CHOICE"]:
        return
    chosen_item = v['CHOICE'][0].strip().split()[0][:-1]
    if (e != "SELECT") or not v['CHOICE']:
        print("pick returning None")
        return
    else:
#       print("\n".join(
#           ["code.textual.pick:",
#           "  line chosen...",
#           f"    {repr(v['CHOICE'])}",
#           "  record returned:",
#           f"    {repr(mappings[int(chosen_item)])}"],
#           ))
        return mappings[int(chosen_item)]

def pick_func(carte, font=font):
    """
    <carte> is a dict with values that are functions.
    User is presented with a choice of all the keys
    and returned in the corresponding function.
    """
    options = [key for key in carte.keys()]
    layout = [
        [sg.Text("Make a Choice", size=(30,1),)],
        [sg.Listbox(values=options, select_mode='extended',
            key='CHOICE', size=(30, len(options)))],
        [sg.Button('SELECT',), sg.Button('CANCEL'),]
            ]
    win = sg.Window("Main Menu", layout, font=font)
    e, v = win.read()
    win.close()
    if (e in (None, 'CANCEL')) or not v or not v["CHOICE"]:
        print(
            "Cancelled or no choice made; aborting main menu")
        return
    return carte[v['CHOICE'][0]]


## Testing Functions:
def ck_pick():
#   print("Running main")
    keys = "statusID, text".split(", ")
    query = """SELECT * FROM stati;"""
    res = pick(query, keys, "{statusID}: {text}")
    print(res)

def ck_change_mapping():
    d = dict(
            first="Alex",
            last="Kleider",
            suffix="NMI",
            )
    new_d = change_mapping(d)
    if isinstance(new_d, dict):
        helpers.show_dict(new_d)
    else:
        print("User aborted.")

def ck_blank_entries_removed():
    d1 = dict(first="Alex", mi="", last="Kleider", suffix="")
    d2 = blank_entries_removed(d1)
    print(d1)
    print(d2)

if __name__ == "__main__":
#   print(yes_no("Do you believe?"))
#   print(yes_no("Do you believe?", font=('Helvetica', 30)))
#   ck_change_mapping()
#   ck_blank_entries_removed()
    ck_pick()

