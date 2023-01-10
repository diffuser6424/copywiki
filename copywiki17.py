import requests
import re
import os

# change working directory
os.chdir("C:/Users/User/Downloads/python folder/")

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
    # Remove the text within <ref> tags
    markdown = re.sub(r"# ", "- ", markdown)
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
    
    # remove trailing pounds
    markdown = remove_trailing_pounds(markdown)
   
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
    
    return markdown

def remove_trailing_pounds(markdown):
    lines = markdown.split("\n")
    lines = [line.rstrip("# ") if line.endswith("# ") else line for line in lines]
    return "\n".join(lines)

def remove_blank_lines_at_start(markdown):
    lines = markdown.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines)

def remove_lines_with_braces(markdown):
    lines = markdown.split("\n")
    lines = [line for line in lines if not line.startswith("{") and not line.startswith("}") and not line.startswith("[[File:") and not line.startswith("[[Image:")]
    return "\n".join(lines)
  
def get_wikipedia_article_markdown(article_title):
  # Replace spaces in the article title with underscores
  article_title = article_title.replace(" ", "_")

  # Make a GET request to the MediaWiki API
  url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&rvprop=content&titles={article_title}"
  response = requests.get(url, verify=False)
  
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
    
    # remove blank lines at the start
    markdown = remove_blank_lines_at_start(markdown)
    
    # modify text
    markdown = modify_text(markdown)
    
    return markdown
  else:
    # If the request is not successful, return an empty string
    return ""

# Output the Markdown content to a .md file
try:
  with open("articles.txt", "r", encoding="utf-8") as f:
    article_titles = f.readlines()
except FileNotFoundError:
  print("Error: The file 'articles.txt' does not exist.")
  exit(1)

article_titles = [title.strip() for title in article_titles]

for article_title in article_titles:
  markdown = get_wikipedia_article_markdown(article_title)
  file_name = article_title.replace("_", " ") + ".md"
  print(file_name)
  with open(file_name, "w", encoding="utf-8") as f:
    f.write(markdown)

print("Done!")