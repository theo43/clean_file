#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 17:30:06 2017
@author: theo43@github
"""

from sys import argv
from re import sub, search, findall, split
from collections import Counter


def clean_tabs(line, line_number, counter):
    """Clean the tabulation(s) detected in a string and replace them with
       four spaces

       Arguments:
           - line (string): content of the line to be treated
           - line_number (int): line number in the file
           - counter (Counter): counts concerned lines and deleted spaces in
             the file

       Returns:
           - line (string): line with tab(s) replaced by four spaces
           - counter (Counter): updated counter

       Example:
           >>> cnt = Counter({'line': 1, 'space':0})
           >>> clean_tabs("\t\ta = 42\t\n", 9, counter=cnt)
           ('        a = 42    \n', Counter({'tab': 4}))

    """

    list_tabs = findall(r"\t", line)
    if len(list_tabs) != 0:
        line = sub(r"\t", " "*4, line)
        counter["tab"] += len(list_tabs)
        if len(list_tabs) == 1:
            print("Line {}: {} tab replaced by spaces"\
                  .format(line_number, len(list_tabs)))
        else:
            print("Line {}: {} tabs replaced by spaces"\
                  .format(line_number, len(list_tabs)))
        return line, counter

    else:
        return line, counter


def clean_end_of_line_spaces(line, line_number, counter, regex=r"[ ]+$"):
    """Search useless spaces at the end of a string and delete them

       Arguments:
           - line (string): content of the line to be treated
           - counter (Counter): counts concerned lines and deleted spaces

       Returns:
           - line (string): line without spaces in the end of the line
           - counter (Counter): updated counter

       Example:
           >>> line = "    def func(beta=0.97):     "
           >>> cnt = Counter({'line': 1, 'space':0})
           >>> clean_end_of_line_spaces(line, 77, counter=cnt)
           ('    def func(beta=0.97):', Counter({'space': 5, 'line': 2}))

    """

    detected = search(regex, line)

    if detected:
        counter["line"] += 1
        spaces_to_delete = len(detected.group())
        counter["space"] += spaces_to_delete
        if spaces_to_delete:
            print("Line {}: {} deleted end-of-line space"\
                  .format(line_number, spaces_to_delete))
        else:
            print("Line {}: {} deleted end-of-line spaces"\
                  .format(line_number, spaces_to_delete))

    # Delete the useless spaces
    line = sub(regex, "", line)

    return line, counter


if __name__ == '__main__':

    # Initialize the counter
    CNT = Counter()

    FILE_NAMES = argv[1:]

    for FILE_NAME in FILE_NAMES:

        print("Read file: {}".format(FILE_NAME))
        FILE_IN = open(FILE_NAME, "r")
        LINES = FILE_IN.readlines()
        FILE_IN.close()

        print("Replace the original file with the clean one? (y/n)")
        AGAIN = True
        while AGAIN:
            CHOICE = input(">>> ")
            if CHOICE == 'y':
                NEW_NAME = FILE_NAME
                print("Clean the file: {}".format(FILE_NAME))
                AGAIN = False
            else:
                if CHOICE == 'n':
                    print("No replacement")
                    NEW_NAME = split(r"\.py", FILE_NAME)[0] + "_clean.py"
                    print("\nCreation of file: {}\n".format(NEW_NAME))
                    AGAIN = False
                else:
                    print("Wrong input: \"y\" or \"n\" only! Try again")

        FILE_OUT = open(NEW_NAME, "w")

        for i, line in enumerate(LINES):
            line, CNT = clean_tabs(line, i, CNT)
            line, CNT = clean_end_of_line_spaces(line, i, CNT)
            FILE_OUT.write(line)

        print("\n" + "*"*60)
        print("Number of replaced tabs: {}".format(CNT["tab"]))
        print("Number of deleted spaces: {}".format(CNT["space"]))
        print("Number of concerned lines: {}\n{}".format(CNT["line"], "*"*60))

        FILE_OUT.close()
