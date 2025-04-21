import os
import datetime
import json
import xml.etree.ElementTree as ET
import sqlite3
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
        db = DatabaseWriter()
        db.save_news(self.text, self.city)
        db.close()

class PrivateAd(NewsFeed):
    def __init__(self, text, expiration_date):
        super().__init__()
        self.text = text
        self.expiration_date = expiration_date
        self.date_left = (datetime.datetime.strptime(self.expiration_date, "%Y-%m-%d") - datetime.datetime.now()).days

    def publish(self):
        content = f"Private Ad -----------------\n{self.text}\nActual until: {self.expiration_date}, {self.date_left} days left"
        self.publish_to_file(content)
        db = DatabaseWriter()
        db.save_ad(self.text, self.expiration_date, self.date_left)
        db.close()

class PerfectQuote(NewsFeed):
    def __init__(self, quote, author):
        super().__init__()
        self.quote = quote
        self.author = author
        self.score = len(quote.split())
    def publish(self):
        content = f"Perfect quote -------------\n{self.quote}\n{self.author}\nScore of words: {self.score}"
        self.publish_to_file(content)
        db = DatabaseWriter()
        db.save_perfect_quote(self.quote, self.author, self.score)
        db.close()

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


class JSONImporter:
    """Handles importing and processing records from a JSON file."""

    def __init__(self, path=None):
        """Initializes with default or user-provided file path."""
        self.file_path = path or "input_records.json"

    def parse_json_records(self):
        """
        Parses records from the JSON input file.
        Returns a list of record objects (News, PrivateAd, MotivationalQuote).
        """
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' not found.")
            return []

        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                records = json.load(file)
            except json.JSONDecodeError:
                print("Invalid JSON format.")
                return []

        parsed_records = []

        for item in records:
            rtype = item.get("type", "").lower()
            if rtype == "news":
                parsed_records.append(News(item.get("text", ""), item.get("city", "")))
            elif rtype == "privatead":
                parsed_records.append(PrivateAd(item.get("text", ""), item.get("expiration", "")))
            elif rtype == "perfectquote":
                parsed_records.append(PerfectQuote(item.get("text", ""), item.get("author", "")))
            else:
                print(f"Unknown record type: {rtype}")

        return parsed_records

    def process_file(self):
        """Parses and publishes all JSON records, then deletes the input file if successful."""
        records = self.parse_json_records()
        if records:
            for record in records:
                record.publish()
            #os.remove(self.file_path)
            print(f"JSON file '{self.file_path}' processed and removed.")
        else:
            print("No valid records found in JSON.")


class XMLImporter:
    """Handles importing and processing records from an XML file."""

    def __init__(self, path=None):
        """Initializes with default or user-provided file path."""
        self.file_path = path or "input_records.xml"

    def parse_xml_records(self):
        """
        Parses XML records and returns a list of record objects.
        Each <record> must contain a <type> element.
        """
        if not os.path.exists(self.file_path):
            print(f"File '{self.file_path}' not found.")
            return []

        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError:
            print("Invalid XML format.")
            return []

        parsed_records = []

        for record_el in root.findall("record"):
            rtype = (record_el.findtext("type") or "").strip().lower()
            text = record_el.findtext("text", "").strip()

            if rtype == "news":
                city = record_el.findtext("city", "").strip()
                parsed_records.append(News(text, city))
            elif rtype == "privatead":
                expiration = record_el.findtext("expiration", "").strip()
                parsed_records.append(PrivateAd(text, expiration))
            elif rtype == "perfectquote":
                author = record_el.findtext("author", "").strip()
                parsed_records.append(PerfectQuote(text, author))
            else:
                print(f"Unknown record type: {rtype}")

        return parsed_records

    def process_file(self):
        """Parses and publishes all XML records, then deletes the input file if successful."""
        records = self.parse_xml_records()
        if records:
            for record in records:
                record.publish()
            os.remove(self.file_path)
            print(f"XML file '{self.file_path}' processed and removed.")
        else:
            print("No valid records found in XML.")


class DatabaseWriter:
    """Handles saving records into SQLite database, avoiding duplicates."""

    def __init__(self, db_path="records.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Creates the necessary tables if they don't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_feed_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                city TEXT,
                date TEXT,
                UNIQUE(text, city, date)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_feed_ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                expiration TEXT,
                date_left INTEGER,
                UNIQUE(text, expiration)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_feed_perfect_quote (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                author TEXT,
                score INTEGER,
                UNIQUE(text, author)
            )
        ''')
        self.conn.commit()

    def save_news(self, text, city, date=None):
        date = date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            self.cursor.execute(
                "INSERT INTO news_feed_news (text, city, date) VALUES (?, ?, ?)",
                (text, city, date)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate news not saved.")

    def save_ad(self, text, expiration, date_left):
        try:
            self.cursor.execute(
                "INSERT INTO news_feed_ads (text, expiration, date_left) VALUES (?, ?, ?)",
                (text, expiration, date_left)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate ad not saved.")

    def save_perfect_quote(self, text, author, score):
        try:
            self.cursor.execute(
                "INSERT INTO news_feed_perfect_quote (text, author, score) VALUES (?, ?, ?)",
                (text, author, score)
            )
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Duplicate quote not saved.")

    def close(self):
        self.conn.close()


def main():
    while True:
        print("Choose what you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Perfect Quote")
        print("4. Import from text file")
        print("5. Import from json file")
        print("6. Import from xml file")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

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
            custom_path = input("Enter text file path (or press Enter to use default): ").strip()
            path = custom_path if custom_path else None
            FileImporter(path).process_file()
        elif choice == "5":
            custom_path = input("Enter json file path (or press Enter to use default): ").strip()
            path = custom_path if custom_path else None
            JSONImporter(path).process_file()
        elif choice == "6":
            custom_path = input("Enter xml file path (or press Enter to use default): ").strip()
            path = custom_path if custom_path else None
            XMLImporter(path).process_file()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")
main()


