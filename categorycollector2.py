# Goal: 
# Author: ChatGPT Jan 9 Edition (operated by User)

import os
import requests

# Change directory
os.chdir("C:/Users/User/Downloads/python folder/")

# Read in the list of categories from the text file
with open('categories.txt', 'r', encoding='UTF-8') as file:
    categories = file.readlines()
    categories = [category.strip() for category in categories]

# Initialize an empty list to store the subcategories
subcategories = []

# Iterate through the list of categories
for category in categories:
    # Make a GET request to the Wikipedia API for the category
    response = requests.get(f'https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle={category}&cmlimit=max')
    # Get the JSON data from the response
    data = response.json()
    # Check if the "query" key is present in the JSON data
    if 'query' not in data:
        print(f'Category {category} does not exist.')
        continue
    # Get the list of subcategories from the JSON data
    subcats = [member['title'] for member in data['query']['categorymembers'] if member['ns'] == 14]
    # Add the subcategories to the list
    subcategories += subcats

# Write the list of subcategories to the text file
with open('subcategories.txt', 'w', encoding='UTF-8') as file:
    for subcategory in subcategories:
        file.write(subcategory + '\n')
        print("printing " + subcategory)
