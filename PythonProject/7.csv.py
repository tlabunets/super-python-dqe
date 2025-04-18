import csv
import string
from collections import Counter

def analyze_text_file(file_path):
    """Analyzes text from the output file and writes 2 CSVs: word and letter stats."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    # --- Word Count CSV ---
    words = [word.lower().strip(string.punctuation) for word in text.split()]
    word_counts = Counter(words)

    with open("word_count.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "count"])
        for word, count in word_counts.items():
            if word:  # ignore empty strings
                writer.writerow([word, count])

    # --- Letter Count CSV ---
    letters = [char for char in text if char.isalpha()]
    letter_counter = Counter(char.lower() for char in letters)
    upper_counter = Counter(char for char in text if char.isupper())
    total_letters = sum(letter_counter.values())

    with open("letter_count.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["letter", "count_all", "count_uppercase", "percentage"])
        for letter in sorted(letter_counter):
            count_all = letter_counter[letter]
            count_upper = upper_counter.get(letter.upper(), 0)
            percentage = round((count_all / total_letters) * 100, 2)
            writer.writerow([letter, count_all, count_upper, f"{percentage}%"])


file_path="news_feed.txt"
analyze_text_file(file_path)
print(f"Generated word_count.csv and letter_count.csv files from {file_path} file")