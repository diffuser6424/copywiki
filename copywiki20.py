# Author: ChatGPT Jan 9 Edition (operated by user)
# Designer: user
# Date Updated: 2023-01-14

# Main function
# - use requests Python module to interact with MediaWiki API
# - read response from API to get content
# - manipulate content for optimization with Obsidian
# - write content to directory where user stores their data


# Optimize content for Obsidian
# - Replace categories with tags
# - Remove HTML inline references
# - Remove trailing pounds (a workaround)
# - Remove lines starting with special characters (removes table data)
 
# Data analysis with Obsidian
# - Obsidian markdown vault with graph and tag plugins enabled.
# - Obsidian opens a file directory, aggregates tags and generates graphs to display relationships between files/articles.
# - I am still searching for use cases and new methods of using mediawiki API.

# Limitations
# - Can not interpret any tables
# - Breaks when given "?", "/", """, and ":". Will currently skip these articles.
# - Skips printing categories as they usually don't associate directly with pages.

# Other functions
# - DirFileNames.py (r=directory, w=filenames.txt)
# - listmaker.py (r=articles.txt, w=articles.txt)
# - pagecollector-simple.py (r=categories.txt, w=categorypages.txt)
# - categorycollector2.py (r=categories.txt, w=subcategories.txt)

# text files separated by newline
# - articles.txt
# - categoryPages.txt
# - categories.txt
# - subcategories.txt
# - filenames.txt

import requests
import re
import os

# change working directory (doc 1)
os.chdir("C:/Users/User/Downloads/python folder/")
line_count = 0
current_line = 1
def replace_category(text):
    pattern = re.compile(r"\[\[Category:([^|]+?)(\|.*?)?\]\]")
    new_text = ""
    last_end = 0
    for match in pattern.finditer(text):
        new_text += text[last_end:match.start()]
        if "|" in match.group(0):
            category_name = match.group(0).split("|")[0][11:]
        else:
            category_name = match.group(1)
        new_text += "#" + category_name.replace(" ", "_").replace("'", "")
        last_end = match.end()
    new_text += text[last_end:]
    return new_text

def modify_text(markdown):
    lines = markdown.split("\n")
    modified_lines = []
    for line in lines:
        # Remove the text within <ref> tags
        # markdown = re.sub(r"# ", "- ", markdown)
        markdown = re.sub(r"<ref.*?>.*?</ref>", "", markdown)
        
        # replace more refs <ref name=":32" /> *?
        markdown = re.sub(r"<ref name=.*?/>", "", markdown)
        markdown = re.sub(r"<ref name=\".*?\">.*?</ref>", "", markdown)

        # modify bold indicator
        markdown = re.sub(r"'''", "**", markdown)
        
        # replace highlighted headers to actual header types
        markdown = re.sub(r"=====", "##### ", markdown)
        markdown = re.sub(r"====", "#### ", markdown)
        markdown = re.sub(r"===", "### ", markdown)
        markdown = re.sub(r"==", "## ", markdown)
    
        # replace math indicators 
        markdown = re.sub(r"<math>", "$", markdown)
        markdown = re.sub(r"</math>", "$", markdown)

        # replace efn stuff {{Efn|
        markdown = re.sub(r"{{Efn.*?}}", "", markdown)
        
        # remove footnotes {{Sfn|Ferguson|2004|p=307}}
        markdown = re.sub(r"{{Sfn.*?}}", "", markdown)
        
        # {{Short description|
        markdown = re.sub(r"{{Short description.*?}}", "", markdown)
        
        # {{Redirect|
        markdown = re.sub(r"{{Redirect.*?}}", "", markdown)
        
        # {{About-distinguish-text|
        markdown = re.sub(r"{{About-distinguish-text.*?}}", "", markdown)
        
        # {{Infobox 
        markdown = re.sub(r"{{Infobox.*?}}", "", markdown)
        
        # append modified_lines to line
        modified_lines.append(line)
        
    return markdown

def remove_trailing_pounds(markdown):
    lines = markdown.split("\n")
    lines = [line.rstrip("# ") if line.endswith("# ") else line for line in lines]
    return "\n".join(lines)

def remove_lines_with_braces(markdown):
    lines = markdown.split("\n")
    lines = [line for line in lines if not line.startswith("{") and not line.startswith("}") and not line.startswith("[[File:") and not line.startswith("[[Image:") and not line.startswith("|") and not line.startswith("File:")]
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines)
  
def main(article_title):
  # Replace spaces in the article title with underscores
  article_title = article_title.replace(" ", "_")

  # Make a GET request to the MediaWiki API
  url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvprop=content&titles={article_title}"
  response = requests.get(url)
  
  # Check the status code of the response
  if response.status_code == 200:
    # If the request is successful, parse the JSON data
    data = response.json()
    pages = data["query"]["pages"]

    # Get the page ID of the article
    page_id = list(pages.keys())[0]
  
    # Get the Markdown content of the article
    markdown = data.get("query", {}).get("pages", {}).get(page_id, {}).get("revisions", [{}])[0].get("*", "")
    
    # replace category links with tags
    markdown = replace_category(markdown)
    
    # remove lines that bein with files or brackets
    markdown = remove_lines_with_braces(markdown)
    
    # modify text
    markdown = modify_text(markdown)
    
    # remove trailing pounds
    markdown = remove_trailing_pounds(markdown)
    
    return markdown
  else:
    # If the request is not successful, return an empty string
    return ""

# Get article titles and line count
try:
  with open("articles.txt", "r", encoding="utf-8") as f:
    article_titles = f.readlines()
    line_count = len(article_titles)
    print("Number of lines:", line_count)
    
except FileNotFoundError:
  print("Error: The file 'articles.txt' does not exist.")
  exit(1)

#not sure what this does, maybe removes spaces?
article_titles = [title.strip() for title in article_titles]

# loop through all articles
for article_title in article_titles:

  # Check for special characters
  if "?" in article_title or "/" in article_title or '"' in article_title or ":" in article_title or "*" in article_title:
    print("Skipping line   (" + str(current_line) + "/" + str(line_count) + "): " + article_title)
    current_line += 1
    continue
  
  # call main function
  markdown = main(article_title)
  # set file name with underscores and .md at the end
  file_name = article_title.replace("_", " ") + ".md"
  print("Writing article" + " (" + str(current_line) + "/" + str(line_count) + "): " + file_name)
  current_line += 1
  # write the content to directory as file_name
  with open(file_name, "w", encoding="utf-8") as f:
    f.write(markdown)
 
# conclusion
print(str(current_line-1) + "/" + str(line_count)+" lines processed.")
