"""
Project:    Kindler
Started:    20/04/2020
Summary:    Scrape your highlights from Kindle's My Clippings.txt
"""

from sys import argv
import os

my_clippings = 'My Clippings.txt' #filename.

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
        lines = getLines() #why call getLines() twice?
        return [i for i, line in enumerate(lines) if line == '==========' and i != len(lines)-1]
        # if no extra delimeter in getLines(), last condition is just len(lines). Which is easier to read?

    def parseDetails(details):
        """Returns location from string of form below. For example below, returns 3578.)
        - Your Highlight on page 222 | location 3576-3578 | Added on Tuesday, 17 September 2019 10:34:09"""
        try:
            return int(details.split()[8].split('-')[1])
        except IndexError:
            return int(details.split()[5])
            print('flop', details)

    lines, units = getLines(), []

    for delimeterIndex in delimeterIndices():
        title = lines[delimeterIndex+1]
        det = lines[delimeterIndex+2]
        # loc = parseDetails(lines[delimeterIndex+2])
        message = lines[delimeterIndex+4]
        units.append((title, det, message))
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

    print("Welcome to kindler.py, use me to scrape your highlights from Kindle's My Clippings.txt")
    print("Here are commands and their descriptions: \n")

    for command, description in features.items():
        print(f"{command} : {description}")


def showTitles():
    "Prints all titles."
    [print(i, title) for i, title in enumerate(getTitles(), start=1)]


def importAsTxt():
    "Imports your clippings as txt file, saves them in ../highlights/{title}.txt"

    def highlightsFrom(title):
        "Returns list of all highlights in given title. Removes duplicates."
        matching_units = filter((lambda unit: title in unit[0]), units)

        highlights = [matching_unit[2]
                      for matching_unit in sorted(matching_units, key=(lambda unit: unit[1]))]
        return set(highlights)

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

    modes = {'help': help, 'showTitles': showTitles,
             'importAsTxt': importAsTxt, 'importAsJSON': importAsJSON}

    try:
        units = getUnits()
    except FileNotFoundError:
        print("Kindler: I can't find your My Clippings.txt file here. Did you paste it? \n")

    try:
        outputs = modes[option]()
    except KeyError:
        print('Invalid option! For help, run: python kindler.py help')
