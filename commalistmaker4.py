import os
os.chdir("C:/Users/User/Downloads/python folder/")
def remove_empty_lines(string):
  # Split the string into a list of lines
  lines = string.split("\n")

  # Filter out the lines that contains filtered text "
  filtered_lines = [line for line in lines if "This section is empty. " not in line and "[icon]" not in line]

  # Join the filtered lines into a single string
  filtered_string = "\n".join(filtered_lines)

  return filtered_string

# Open the file in read mode
with open('articles.txt', 'r') as file:
  # Read the contents of the file
  contents = file.read()

# Replace the commas with newlines
modified_contents = contents.replace(", ", "\n")

# Replace the hyphens with newlines
modified_contents = modified_contents.replace("-", "\n")

# Remove the lines that contain "[icon]"
filtered_contents = remove_empty_lines(modified_contents)

# Remove the lines that contain "This section is empty. "
filtered_contents = remove_empty_lines(filtered_contents)

# Split the modified contents into a list of lines
lines = filtered_contents.split("\n")

# Filter out the lines that are shorter than 5 characters
filtered_lines = [line for line in lines if len(line) >= 5]

# Join the filtered lines into a single string
final_contents = "\n".join(filtered_lines)

# Open the file in write mode
with open('articles.txt', 'w') as file:
  # Write the final contents to the file
  file.write(final_contents)
