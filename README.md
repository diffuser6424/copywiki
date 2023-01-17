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

## Overview

### Main function

#### Description

- use requests Python module to interact with MediaWiki API
- read response from API to get content
- manipulate content for optimization with Obsidian
- write content to directory where user stores their data

#### Sequence

`Copywiki20.py`

- Execute `copywiki`
- Try to open `articles.txt` in read mode with UTF-8 encoding
	- Write article titles to list `article_titles`
	- Set `line_count` to `len(article_titles)`
	- Output `line_count`
- Set `article_titles` to `[title.strip() for title in article_titles]`
- Loop `for article_title in article_titles` list
	- Check for certain characters like "?" and ":" in `article_title`
	- Call function `main`
		- Get `response = requests.get(url)`
		- Set `data = response.json()`
		- Set `pages = data["query"]["pages"]`
		- Set `page_id = list(pages.keys())[0]`
		- Get`markdown = data.get("query", {}).get("pages", {}).get(page_id, {}).get("revisions", [{}])[0].get("*", "")`
		- Call function `replace_category`
		- Call function `remove_lines_with_braces`
		- Call function `modify_text`
		- Call function `remove_trailing_pounds`
		- return `markdown`
	- Set `file_name` to `article_title.replace("_", " ") + ".md"`
	- Output progress and iterate `current_line`
	- write `markdown` to directory with UTF-8 encoding as `file_name`
- Print `current_line` / `line_count` “lines processed”.

### Optimize content for Obsidian

- Replace categories with tags
- Remove HTML inline references
- Remove trailing pounds (a workaround)
- Remove lines starting with special characters (removes table data)
 
### Limitations

- Can not interpret any tables
- Breaks when given "?", "/", """, and ":". Will currently skip these articles.
- Skips printing categories as they usually don't associate directly with pages.

### Other functions

- DirFileNames.py (r=directory, w=filenames.txt)
- listmaker2.py (r=articles.txt, w=articles.txt)
- pagecollector-simple.py (r=categories.txt, w=categorypages.txt)
- categorycollector2.py (r=categories.txt, w=subcategories.txt)

### text files separated by newline

- articles.txt
- categoryPages.txt
- categories.txt
- subcategories.txt
- filenames.txt

## Product

Data analysis with Obsidian
- Obsidian markdown vault with graph and tag plugins enabled.
- Obsidian opens a file directory, aggregates tags and generates graphs to display relationships between files/articles.
- I am still searching for use cases and new methods of using mediawiki API.

## 2023-01-10
I'm trying to get the categories to turn into tags. I think plugins in other vaults might be effecting the speed of my other vaults. It seems like this vault is loading faster since I disabled some plugins in the bookmarks vault.

I made ChatGPT replace Category links with tags.

## 2023-01-11

articles that have titles that contain special characters are not being processed correctly. Including "/".

looks like comments and other uses of the "<" and ">" characters will break the article.

## 2023-01-13

okay so today we have a pagecollector-simple.py it takes a categories.txt which is a list of Wikipedia categories, separated by newlines. the page collector will then get each page linked to that category and print it to categorypages.txt before moving on to the next category in the list.

`copywiki17.py` takes Wikipedia page/article titles and prints them to markdown files (and making many modification to the text to make it Obsidian friendly). It reads `articles.txt` and writes to a specified directory.

`listmaker2.py` takes a messy list of Wikipedia article/page titles and removes extra characters, making it easier for `copywiki17.py` to read. It reads and writes to `articles.txt`.

`pagecollector-simple.py` takes a list of Wikipedia categories and writes the title of all articles/pages inside the category (excluding subcategories). It reads `categories.txt` and writes the titles to `categorypages.txt`

`categorycollector.py` should take a list of categories and print a list of sub categories. It should read `categories.txt` and print the list of subcategories to `subcategories.txt`

Okay so in `copywiki19.py` I was able to add a loading print out for each articles. I was also able to skip any lines containing the three characters that always cause issues, "?" "/" and """.

## 2023-01-15

what if I was able to grab the subcategories and write them in a way that Obsidian Nested Tags feature would understand. That would allow me to see not only the structure of the articles but now the structure of the categories. I could also try to create a canvas starting with the outline and timeline and then going to the topmost categories and pages.

## 2023-01-16

I want page and category collector to not have separate text files. 
I also want them to overwrite any content and not append. 
I want all the functions in the same .py file. 
I want nested tag functionality. 
I want a counter and a current line display for page and category collector. 
I want uniform names so that Github can handle file history instead of iterating the filename. 
I want an obsidian vault to automatically be created and for copywiki to output the files into the chosen vault directory.

perhaps instead of categories.txt I could ask the user to input a category

I would like to combine the functions in `main`.

### Current `copywiki` sequence

- Execute `copywiki`
- Try to open `articles.txt` in read mode with UTF-8 encoding
	- Write article titles to list `article_titles`
- Open `articles.txt` in read mode with UTF-8 encoding
- Set `int lines` to `f.read().splitlines()`
- Set `line_count` to `len(lines)`
- Output `line_count`
- Set `article_titles` to `[title.strip() for title in article_titles]`
- Loop `for article_title in article_titles` list
	- Call function `get_wikipedia_article_markdown`
		- Call function `replace_category`
		- Call function `remove_lines_with_braces`
		- Call function `remove_blank_lines_at_start`
		- Call function `modify_text`
			- Call function `remove_trailing_pounds`
	- Check for certain characters like "?" and ":" in `article_title`
	- Set `file_name` to `article_title.replace("_", " ") + ".md"`
	- Output progress and iterate `current_line`
	- write `markdown` to directory with UTF-8 encoding as `file_name`
- Print `current_line` / `line_count` “lines processed”.

### list of functions

- def replace_category(text):
- def modify_text(markdown):
- def remove_trailing_pounds(markdown):
- def remove_blank_lines_at_start(markdown):
- def remove_lines_with_braces(markdown):
- def get_wikipedia_article_markdown(article_title):

### Future `copywiki` sequence

- User prompted for input → “category title” → writes to `categories.txt`
- Execute `categoryCollector.py`, uses `categories.txt` to append subcategories to `categories.txt`
- Execute `pagecollector.py` uses `categories.txt` to overwrite article titles to `articles.txt`

==Are you sure you want to overwrite `articles.txt`?==

==Are you sure you want to append `categories.txt`?==

## 2023-01-17

- `categorycollector2.py` is case-sensitive
