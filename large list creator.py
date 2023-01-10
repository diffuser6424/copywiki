from pathlib import Path
import os

# change working directory
os.chdir("C:/Users/User/Downloads/python folder/")

# get the current working directory
cwd = os.getcwd()

# open the file for writing
with open('large_list.txt', 'w', encoding='utf-8') as f:
    # list all files in the directory
    for filename in os.listdir(cwd):
        if os.path.isfile(os.path.join(cwd, filename)):
            # write the filename to the file
            f.write(filename + "\n")

