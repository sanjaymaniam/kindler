Free your highlights from Kindle's `My Clippings.txt`.


How To Get Help:
1. Clone this repository.
2. Run `python kindler.py help`.
3. Kindler will tell you what it can do for you. Remember this command, saves a ton of time.

How To Get All Your Highlights:
1. Clone this repository. Paste your My Clippings.txt file in it.
2. Run `python kindler.py importAsTxt`.
3. Kindler makes a folder `/highlights` in your working directory. Open it.
4. Pow! Your highlights are in text files named after the book's title.

How To Get List Of Titles:
1. Clone this repository. Paste your My Clippings.txt file in it.
2. Run `python kindler.py showTitles`.
3. There! Your titles are printed on terminal.

To Do:
- ~Sort highlights by location.~
- Sort highlights by datetime.
- Avoid extra delimeter in getLines() by indexing properly.
- **Build importAsJSON for webapps.**
