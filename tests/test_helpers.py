#!/usr/bin/env python3

# File: tests/test_helpers.py

"""
Run pytest in the following way 
PYTHONPATH=src pytest
"""

import helpers

mapping = dict(
        one= "uno",
        two= "duo",
        three= "tres",
        )

def test_show_dict():
    assert helpers.show_dict(mapping) == [
            "one: uno",
            "two: duo",
            "three: tres",
            ]

def donothing():
    pass

if __name__ == "__main__":
#   test_show_dict()
    donothing()

