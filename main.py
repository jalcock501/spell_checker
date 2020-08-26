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
    corrected = spellcheck(data)  # spell checking function
    write_csv(corrected)


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


def write_csv(corrected):
    with open(os.path.join(_basedir,
                           _datafolder,
                           'correct.csv'),
              'w+') as writehandle:
        writer = csv.writer(writehandle)
        for row in corrected:
            writer.writerow(row)


# ------------------- SPELL CHECKING ------------------------
# Check spelling of each work in any given list
def spellcheck(data):
    corrected = []
    spell = enchant.Dict('en-US')

    for i in data:  # for row in data
        if len(corrected) == 0:  # ignore header for correction
            corrected.append(i)
            continue
        row = []
        for j in i:  # for column in row
            column = []
            j = j.split()  # split string into list of words
            if len(j) > 1:  # if more than one word
                for k in j:  # for word in sentence
                    # this needs to be better had to add len check
                    # because non alpha chars mess up first len check
                    if not spell.check(k) and len(k) > 1:
                        column.append(spell.suggest(k)[0])
                        continue
                    else:
                        column.append(k)
                row.append(' '.join(column))
            else:  # only one word so no loop needed
                if not spell.check(j[0]):
                    row.append(spell.suggest(j[0])[0])
                    continue
                else:
                    row.append(j[0])
        corrected.append(row)

    return corrected


if __name__ == '__main__':
    main()  # run main function
