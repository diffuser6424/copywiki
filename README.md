# copywiki
Wikipedia scraper using mediawiki API and Requests python module.

## Intro
The goal is to parse Wikipedia articles and then manipulate the text to be accessible in markdown format (the source is in mediawiki format).
I am aware that wikipedia_parser, wikipediaapi, mwparserfromhell, and BeautifulSoup exist but this is me attempting to use just requests module.

## Use
1. Open `copywiki12.py` with VS Code.
2. Edit `articles.txt` (in the same directory as python file) to include a list of articles you want parsed, separated by newline.
3. Select "Run Python File", in VS Code.
4. Check Obsidian vault for newly outputted markdown files.
