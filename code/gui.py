#!/usr/bin/env python3

# File: Projects/868dir/code/gui.py

"""
Collecting what's useful in Git/Sql/Code/textual.py and refining it
"""

import PySimpleGUI as sg

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

## Utility Functions:

def show_dict(mapping):
    for key, value in mapping.items():
        print(f"{key}: {value}", end = '; ')
    print()

## Testing Functions:
def ck_change_mapping():
    d = dict(
            first="Alex",
            last="Kleider",
            suffix="NMI",
            )
    new_d = change_mapping(d)
    if isinstance(new_d, dict):
        show_dict(new_d)
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
    ck_blank_entries_removed()

