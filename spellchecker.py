#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# by jim @ 26/08/2020

# IMPORTS
import sys
import os
import csv
import enchant
from datetime import datetime
import multiprocessing

# PROGRAM VARS
PROG_NAME = __file__  # spellchecker.py
PROG_VERS = '1.0'  # none production version

# GLOBALS
_basedir = os.path.abspath(os.path.dirname(__file__))  # get relative directory
_datafolder = 'data'  # data directory
_datafile = 'example_data1.csv'  # data file
_correctfile = 'correct.csv'


# MAIN FUNCTION
def main():

    with multiprocessing.Manager() as manager:  # use manager for concurrent list
        corrected = manager.list()  # list object from manager class
        processes = []  # empty list for processes
        processors = multiprocessing.cpu_count()  # processor count

        data = read_file()  # csv reader function
        chopped_list = list_divider(data, processors)  # divide list based on cpu count
        start = datetime.now()  # for timing speed
        for n in range(0, processors):
            # create a process for each available processor
            p = multiprocessing.Process(target=spellcheck, args=(chopped_list[n], corrected,))
            processes.append(p)
            p.start()

        # close processes once done
        for process in processes:
            p.join()

        end = datetime.now()
        write_csv(corrected)  # write to file

        print(end - start)


# ------------------- CSV HANDLING --------------------------
# Read csv file and return list of data
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
              'w+', newline='') as writehandle:
        writer = csv.writer(writehandle)
        for row in corrected:
            writer.writerow(row)


# ------------------- SPELL CHECKING ------------------------
# Check spelling of each work in any given list
def spellcheck(data, corrected):
    spell = enchant.Dict('en-US')

    for i in data:  # for row in data
        if len(corrected) == 0:
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


# Divide list based on CPU count
def list_divider(_list: list, n: int):

    avg = len(_list) / float(n)
    out = []

    last = 0.0

    while last < len(_list):
        out.append(_list[int(last): int(last + avg)])
        last += avg

    return out



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
            print("No output file specified outputting to: {}".format(_correctfile))

    main()  # run main function

