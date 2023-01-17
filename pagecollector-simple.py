# Goal:  
# Author: ChatGPT Jan 9 Edition (operated by User)
import requests
import os

os.chdir("C:/Users/User/Downloads/python folder/")

# Open the categories file
with open("categories.txt", "r", encoding='UTF-8') as file:
    categories = file.readlines()

# Iterate through the list of categories
for category in categories:
    category = category.strip()
    cmcontinue = ""
    while True:
        # Make an API call to get the pages in the category
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle={category}&format=json&cmcontinue={cmcontinue}"
        response = requests.get(url, timeout=30)
        data = response.json()

        # Extract the page titles from the API response
        for page in data["query"]["categorymembers"]:
            title = page["title"]
            # Write the title to the output file
            with open("categorypages.txt", "a", encoding='UTF-8') as file:
                file.write(title + "\n")
                print ("Writing to file: " + title)
        if "continue" not in data:
            break
        cmcontinue = data["continue"]["cmcontinue"]
