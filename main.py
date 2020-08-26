#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# by jim @ 26/08/2020

# IMPORTS
import sys
import os
import csv
import enchant

# PROGRAM VARS
PROG_NAME = __file__  # main.py
PROG_VERS = '0.1'  # none production version

# GLOBALS
_basedir = os.path.abspath(os.path.dirname(__file__))  # get relative directory
_datafolder = 'data'  # data directory
_exampledata = 'example_data1.csv'  # data file


# MAIN FUNCTION
def main():
    data = read_file()  # csv reader function
    spellcheck(data)  # spell checking function


# ------------------- CSV HANDLING --------------------------
# Read csv file and return list of data
# TODO: turn this into a generator
def read_file():
    data = []

    # auto close on return with 'with' function
    with open(os.path.join(_basedir,
                           _datafolder,
                           _exampledata),
              'r') as readhandle:
        csvhandle = csv.reader(readhandle)  # use csv library reader function

        for row in csvhandle:  # append out of reader class
            data.append(row)

    return data


# ------------------- SPELL CHECKING ------------------------
# Check spelling of each work in any given list
# TODO: work on better word splitting algorithm
def spellcheck(data):
    spell = enchant.Dict('en-US')

    for i in data:  # for row in data
        for j in i:  # for column in row
            j = j.split()  # split string into list of words
            if len(j) > 1:  # if more than one word
                for k in j:  # for word in sentence
                    # this needs to be better had to add len check
                    # because non alpha chars mess up first len check
                    if not spell.check(k) and len(k) > 1:
                        print(spell.suggest(k))
            else:  # only one word so no loop needed
                if not spell.check(j[0]):
                    print(spell.suggest(j[0]))


if __name__ == '__main__':
    main()  # run main function
