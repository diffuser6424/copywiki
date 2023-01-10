import os
import codecs
import re

os.chdir("C:/Users/User/Downloads/python folder/")
# Open the file in read mode
with open('articles.txt', 'r', encoding='UTF-8') as file:
  # Read all lines in the file
  lines = file.readlines()

# Open the file in write mode
with open('articles.txt', 'w', encoding='UTF-8') as file:
  # Iterate through all lines in the file
  for line in lines:
    # Check if the line is empty or contains "(Level", "article)", or "articles)"
    if len(line) >= 5 and line.strip() and "(Level" not in line and "article)" not in line and "articles)" not in line and ", see " not in line and "other categories" not in line and "See also" not in line and "This list" not in line:
      file.write(line)
# re.sub(r"?", "", 'articles.txt')
