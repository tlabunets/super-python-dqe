import datetime
import os
from functions_4 import normalize_text2

class NewsFeed:
    def __init__(self, filename="news_feed.txt"):
        self.filename = filename

    def publish_to_file(self, content):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(content + "\n\n")
        print("Record published successfully!\n")

class News(NewsFeed):
    def __init__(self, text, city ):
        super().__init__()
        self.text = text
        self.city = city
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def publish(self):
        content = f"News -----------------------\n{self.text}\n{self.city}, {self.date}"
        self.publish_to_file(content)

class PrivateAd(NewsFeed):
    def __init__(self, text, expiration_date):
        super().__init__()
        self.text = text
        self.expiration_date = expiration_date
        self.date_left = (datetime.datetime.strptime(self.expiration_date, "%Y-%m-%d") - datetime.datetime.now()).days

    def publish(self):
        content = f"Private Ad -----------------\n{self.text}\nActual until: {self.expiration_date}, {self.date_left} days left"
        self.publish_to_file(content)

class PerfectQuote(NewsFeed):
    def __init__(self, quote, author):
        super().__init__()
        self.quote = quote
        self.author = author
        self.score = len(quote.split())
    def publish(self):
        content = f"Perfect quote -------------\n{self.quote}\n{self.author}\nScore of words: {self.score}"
        self.publish_to_file(content)

class FileImporter:
    """Handles importing and processing records from a text file."""

    def __init__(self, path=None):
        """Initializes with default or user-provided file path."""
        self.file_path = path or "input_records.txt"

    def parse_records(self):
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' not found.")
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            raw_data = file.read()

        records = raw_data.strip().split("===\n")
        parsed_records = []

        for record in records:
            """
            Parses records from the input file based on predefined format.
            Returns a list of record objects (News, PrivateAd, PerfectQuote).
            """
            lines = [line.strip() for line in record.strip().split("\n") if line.strip()]
            record_dict = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(":", 1)
                    record_dict[key.strip().lower()] = value.strip()

            rtype = record_dict.get("type", "").lower()

            if rtype == "news":
                parsed_records.append(News(normalize_text2(record_dict.get("text", "")), record_dict.get("city", "")))
            elif rtype == "privatead":
                parsed_records.append(PrivateAd(normalize_text2(record_dict.get("text", "")), record_dict.get("expiration", "")))
            elif rtype == "perfectquote":
                parsed_records.append(PerfectQuote(normalize_text2(record_dict.get("text", "")), record_dict.get("author", "")))
            else:
                print(f"Unknown record type: {rtype}")

        return parsed_records

    def process_file(self):
        """Parses and publishes all records, then deletes the input file if successful."""
        records = self.parse_records()
        if records:
            for record in records:
                record.publish()
           # os.remove(self.file_path)
            print(f"File '{self.file_path}' processed and removed.")
        else:
            print("No valid records found.")


def main():
    while True:
        print("Choose what you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Perfect Quote")
        print("4. Import from file")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            text = input("Enter news text: ").strip()
            city = input("Enter city: ").strip()
            News(text, city).publish()
        elif choice == "2":
            text = input("Enter ad text: ").strip()
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ").strip()
            PrivateAd(text, expiration_date).publish()
        elif choice == "3":
            quote = input("Enter your quote: ").strip()
            author = input("Enter author: ").strip()
            PerfectQuote(quote, author).publish()
        elif choice == "4":
            custom_path = input("Enter file path (or press Enter to use default): ").strip()
            path = custom_path if custom_path else None
            FileImporter(path).process_file()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
main()


