from models import Quote, Author
from connect import connect_to_db


def quote_finder():
    while True:
        connect_to_db()
        command = input("Enter command (name: <author>, tag: <tag>, tags: <tag1>, <tag2>, ..., exit): ")
        if command.startswith("name:"):
            author_name = command.split("name:")[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                # name: Steve Martin
                print(f"Searching for author: {author_name}")
                print(f"Author found: {author.fullname}")
                quotes = Quote.objects(author=author)
                data = ([i.to_mongo().to_dict() for i in quotes])
                quotes = [item['quote'] for item in data]
                print(quotes)
            else:
                print(f"Author '{author_name}' not found.")

        elif command == "exit":
            print("Program closed.")
            break
        else:
            print("Invalid command, try again.")


if __name__ == "__main__":
    quote_finder()
