import os
import codecs
import re

os.chdir("C:/Users/User/Downloads/python folder/")

def remove_parentheses(filepath):
    with open(filepath, "r", encoding='ISO-8859-1') as f:
        text = f.read()
        # text = re.sub(r'\()\)', '', text)
        text = re.sub(r'(.*?)\((.*?,.*?)\)', r'\1', text) # thius olne
        # text = re.sub(r'(.*?)\((.*?,.*?)\)', '', text)
        # text = re.sub(r'(.*? P)', r'\1', text)
        # text = re.sub(r'/', '', text)
        # text = re.sub(r'\?', '', text)
        # (.*? P)
        f.close()
    with open(filepath, "w") as f:
        f.write(text)
        f.close()

remove_parentheses("C:/Users/ReedEthan/Downloads/python folder/articles.txt")

with open('articles.txt', 'r', encoding='ISO-8859-1') as file:
  # Read all lines in the file
  lines = file.readlines()
  
  # re.sub(r"(.*?,.*?)", "", 'articles.txt')

# Open the file in write mode
with open('articles.txt', 'w', encoding='ISO-8859-1') as file:
  # Iterate through all lines in the file
  for line in lines:
    # Check if the line is empty or contains "(Level", "article)", or "articles)"
    if len(line) >= 5 and line.strip() and "(Level" not in line and "article)" not in line and "articles)" not in line and ", see " not in line and "other categories" not in line and "See also" not in line and "This list" not in line:
      file.write(line)
      # re.sub(r"?", "", 'articles.txt')
      # re.sub(r"/", "", 'articles.txt')
      # re.sub(r"(.*?,.*?)", "", 'articles.txt')



