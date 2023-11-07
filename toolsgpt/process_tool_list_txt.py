
#English  manually  added to txt
#Spanish  manually  added to txt
import re

input_file = "tools.txt"
output_file = "tools_preprocessed.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

modified_lines = [line.split(":")[-1].strip() for line in lines]

words = ' '.join(modified_lines).split()

filtered_words = [re.sub(r'[\(\),]', '', word) for word in words if not re.match(r'^[a-z]', word)]

unique_words = list(set(filtered_words))

final_words = [word.rstrip('.') for word in unique_words]

with open(output_file, "w") as file:
    file.write("\n".join(final_words))

print("Text processing completed. Modified lines are saved in", output_file)
