import random
import string
import re
########################### Refactoring of string ################

# Text into variable
text = '''tHis iz your homeWork, copy these Text to variable.\n\n
You NEED TO normalize it fROM letter CASEs point oF View. also, 
create one MORE senTENCE witH LAST WoRDS of each existING SENtence 
and add it to the END OF this Paragraph.\n\n
it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.\n\n
last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, 
not only Spaces, but ALL whitespaces. I got 87.'''

# Normalize text
text = text.lower()

# Replace "iz" to "is", if "iz" is not in quotes
text = re.sub(r'(?<![“"])iz(?![”"])', 'is', text)

# Split text to sentences
sentences = re.split(r'([.!?])', text)

words = []
for i in range(len(sentences)):
    sentences[i] = sentences[i].strip().capitalize() #capitalize every sentence
    word = sentences[i].split() # Split every sentence to words
   # print(word[-1])
    if not word:
        continue
    if word[-1] != '.':
       words.append(word[-1]) # Take last word from every sentence and add into separate sentence
text = ' '.join(sentences)
print(text)
print(' '.join(words).capitalize())

whitespace_count = len(re.findall(r'\s', text))
print('Number of whitespaces is ', whitespace_count)


############################ Refactoring of collection ############################
def generate_random_dicts():
    num_dicts = random.randint(2, 10)  # Random number of dictionaries (2 to 10)
    dicts_list = []

    for _ in range(num_dicts):
        num_keys = random.randint(1, 5)  # Random number of keys (1 to 5 per dict)
        keys = random.sample(string.ascii_lowercase, num_keys)  # Unique random letters as keys
        random_dict = {key: random.randint(0, 100) for key in keys}  # Assign random values (0-100)
        dicts_list.append(random_dict)

    return dicts_list


def merge_dicts(dicts_list):
    merged_dict = {}  # Dictionary to store merged values
    key_info = {}  # Dictionary to track max values and corresponding dict index

    # Iterate through each dictionary and store the max value for each key
    for i, d in enumerate(dicts_list):
        for key, value in d.items():
            if key not in merged_dict or value > merged_dict[key]:  # Take max value
                merged_dict[key] = value
                key_info[key] = i + 1  # Store dict index (1-based)

    # Rename keys if they exist in multiple dictionaries
    final_dict = {f"{key}_{key_info[key]}" if sum(1 for d in dicts_list if key in d) > 1 else key: merged_dict[key]
                  for key in sorted(merged_dict.keys())}

    return final_dict

# Example usage
random_dicts = generate_random_dicts()
print("Generated list of dictionaries:", random_dicts)
#random_dicts = [{'k': 1}, {'a': 5}, {'a': 8}, {'g': 7}] # example of repeatable key
merged_result = merge_dicts(random_dicts)
print("Merged dictionary:", merged_result)
