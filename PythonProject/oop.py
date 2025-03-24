import datetime
import os


class NewsFeed:
    def __init__(self, filename="news_feed.txt"):
        self.filename = filename

    def publish_to_file(self, content):
        with open(self.filename, "a", encoding="utf-8") as file:
            file.write(content + "\n\n")
        print("Record published successfully!\n")


class News(NewsFeed):
    def __init__(self, text, city):
        super().__init__()
        self.text = text
        self.city = city
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def publish(self):
        content = f"News:\n{self.text}\n{self.city}, {self.date}"
        self.publish_to_file(content)


class PrivateAd(NewsFeed):
    def __init__(self, text, expiration_date_str):
        super().__init__()
        self.text = text
        try:
            self.expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
            self.days_left = (self.expiration_date - datetime.datetime.now()).days
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            self.days_left = None

    def publish(self):
        if self.days_left is not None:
            content = f"Private Ad:\n{self.text}\nExpires on: {self.expiration_date.strftime('%Y-%m-%d')}, {self.days_left} days left"
            self.publish_to_file(content)


class MotivationalQuote(NewsFeed):
    def __init__(self, quote, author):
        super().__init__()
        self.quote = quote
        self.author = author
        self.popularity_score = len(quote.split())  # Number of words as a simple metric

    def publish(self):
        content = f"Motivational Quote:\n\"{self.quote}\"\n- {self.author} (Popularity Score: {self.popularity_score})"
        self.publish_to_file(content)


def main():
    while True:
        print("Choose what you want to add:")
        print("1. News")
        print("2. Private Ad")
        print("3. Motivational Quote")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            text = input("Enter news text: ").strip()
            city = input("Enter city: ").strip()
            News(text, city).publish()
        elif choice == "2":
            text = input("Enter ad text: ").strip()
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ").strip()
            PrivateAd(text, expiration_date).publish()
        elif choice == "3":
            quote = input("Enter your motivational quote: ").strip()
            author = input("Enter author: ").strip()
            MotivationalQuote(quote, author).publish()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
