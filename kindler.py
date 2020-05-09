"""
Project:    Kindler
Started:    20/04/2020
Summary:    Scrape your highlights from Kindle's My Clippings.txt
"""

import os
from sys import argv

my_clippings = 'My Clippings.txt'  # filename.


def getLines():
    "Returns list of all lines from file. Extra delimeter is added to beginning."
    file = open(my_clippings, 'r', encoding='utf-8-sig')
    # can avoid extra delimeter by indexing properly
    return ['=========='] + [line.strip() for line in file]


def getUnits():
    """Returns list of all 'units'.
    A unit is a tuple with (title, details, message), NOT a highlight. Highlights and notes are messages."""

    def delimeterIndices(delimeter='=========='):
        "Returns indices of lines with delimeter. We use this to identify individual highlights."
        lines = getLines()  # why call getLines() twice?
        return [i for i, line in enumerate(lines) if line == '==========' and i != len(lines)-1]
        # if no extra delimeter in getLines(), last condition is just len(lines). Which is easier to read?

    def parseDetails(details):
        "Returns tuple (kind_of_unit, location). For locations of type '100-123', we take 100."
        listed_details = details.split()
        return(listed_details[2], int(f"{listed_details[8] if 'on' not in listed_details[8] else listed_details[5]}".split('-')[0]))

    lines, units = getLines(), []

    for delimeterIndex in delimeterIndices():
        title = lines[delimeterIndex+1]
        # (highlight/note/bookmark, location)
        details = parseDetails(lines[delimeterIndex+2])
        message = lines[delimeterIndex+4]
        units.append((title, details, message))
    return units


def getTitles():
    "Returns alphabetically sorted list of titles. Removes duplicates."
    # to-do: allow sorting using keys- last read or alphabetically.
    from string import ascii_letters
    titles = []
    for unit in units:
        title = unit[0]
        # handling titles that start with u'\ufeff'.
        if title[0] not in ascii_letters:
            titles.append(title[1:])
        else:
            titles.append(title)
    return sorted(list(set(titles)))


def help():
    features = {'showTitles': 'Show all the titles in your clipping.',
                'importAsTxt': 'Import your highlights as .txt in ../highlights.',
                'importAsJSON': 'Import your highlights as JSON.'}

    print("Welcome to kindler.py, use me to scrape your highlights from Kindle's My Clippings.txt \n")
    print("Here are commands and their descriptions: \n")

    for command, description in features.items():
        print(f"{command} : {description}")


def showTitles():
    "Prints all titles."
    [print(i, title) for i, title in enumerate(getTitles(), start=1)]


def importAsTxt():
    "Imports your clippings as txt file, saves them in ../highlights/{title}.txt"

    def highlightsFrom(title):
        "Returns set of all highlights in given title. Removes duplicates."
        matching_units = filter((lambda unit: title in unit[0]), units)
        temp = sorted(matching_units, key=(lambda x: x[1][1]))
        highlights = [unit[2] for unit in temp]
        return highlights

    def makeFile(title):
        cwd = os.path.abspath(os.curdir)
        directory = f'{cwd}/highlights'
        if not os.path.exists(directory):
            os.makedirs(directory)
        return open(os.path.join(cwd, f'highlights/{title}.txt'), 'w')

    for title in getTitles():
        outfile = makeFile(title)
        for highlight in highlightsFrom(title):
            outfile.write(highlight)
            outfile.write('\n')
        outfile.close()
    print(
        f"I've saved {len(units)} highlights, notes and bookmarks from {len(getTitles())} titles in /highlights. You're welcome!")


def importAsJSON():
    return None


if __name__ == "__main__":
    option = argv[1]

    modes = {'showTitles': showTitles,
             'importAsTxt': importAsTxt, 'importAsJSON': importAsJSON}

    if option == 'help':
        help()
    else:
        try:
            units = getUnits()
            try:
                outputs = modes[option]()
            except KeyError:
                print('Invalid option! For help, run: python kindler.py help')
        except FileNotFoundError:
            print(
                "Kindler: I can't find your My Clippings.txt file here. Did you paste it? \n")
