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
_datafile = 'example_data1.csv'  # data file


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
    try:
        with open(os.path.join(_basedir,
                               _datafolder,
                               _datafile),
                  'r') as readhandle:
            csvhandle = csv.reader(readhandle)  # use csv library reader function

            for row in csvhandle:  # append out of reader class
                data.append(row)
    except FileNotFoundError:
        print("WARNING NO FILE FOUND!")
        print(usage)
        sys.exit(0)

    return data


def write_csv(corrected):
    with open(os.path.join(_basedir,
                           _datafolder,
                           _correctfile),
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
        row = []  # used to recreate row for write
        for j in i:  # for column in row
            column = []  # used to recreate column for write
            j = j.split()  # split string into list of words
            if len(j) > 1:  # if more than one word
                for k in j:  # for word in sentence
                    # this needs to be better had to add len check
                    # because non alpha chars mess up first len check
                    if not spell.check(k) and len(k) > 1:
                        column.append(spell.suggest(k)[0])  # add to column
                        continue
                    else:
                        column.append(k)  # add to column
                row.append(' '.join(column))
            else:  # only one word so no loop needed also means new column
                if not spell.check(j[0]):
                    row.append(spell.suggest(j[0])[0])
                    continue
                else:
                    row.append(j[0])
        corrected.append(row)

    return corrected


if __name__ == '__main__':

    usage ="""
            Usage: --\n 
                spellchecker.py {input} {output}\n
                running spellchecker.py with no args\n
                returns in running test file example_data1.csv\n
            """

    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(usage)
            sys.exit(0)
        _datafolder = ''
        _datafile = sys.argv[1]

        try:
            _correctfile = sys.argv[2]
        except IndexError:
            _correctfile = 'correct.csv'
            print("No output file specified outputting to: {}".format(_correctfile))

    main()  # run main function

