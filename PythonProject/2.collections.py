import random
import string


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
    final_dict = {f"{key}_{key_info[key]}" if sum(k == key for d in dicts_list for k in d) > 1 else key: value
                  for key, value in merged_dict.items()}

    return final_dict


# Example usage
random_dicts = generate_random_dicts()
print("Generated list of dictionaries:", random_dicts)
#random_dicts = [{'a': 5}, {'a': 8}, {'g': 7}] # example of repeatable key
merged_result = merge_dicts(random_dicts)
print("Merged dictionary:", merged_result)
