from models import Quote, Author
from connect import connect_to_db
import sys


def quote_finder():
    while True:
        connect_to_db()
        command = input("Enter command (name: <author>, tag: <tag>, tags: <tag1>, <tag2>, ..., exit): ")
        if command.startswith("name:"):
            author_name = command.split("name:")[1].strip()
            author = Author.objects(fullname=author_name).first()
            if author:
                quotes = Quote.objects(author=author)
                if quotes:
                    print(f"Quotes of author {author.fullname}:")
                    for quote in quotes:
                        print(quote.quote.encode('utf-8'))
                else:
                    print("No quotes found for author:", author_name)
            else:
                print(f"Author '{author_name}' not found.")
        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            quotes = Quote.objects(tags=tag)
            if quotes:
                print(f"Quotes with tag '{tag}':")
                for quote in quotes:
                    print(quote.quote.encode('utf-8'))
            else:
                print("No quotes found with tag:", tag)
        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip().split(',')
            quotes = Quote.objects(tags__in=tags)
            if quotes:
                print(f"Quotes with tags '{', '.join(tags)}':")
                for quote in quotes:
                    print(quote.quote.encode('utf-8'))
            else:
                print("No quotes found with tags:", ', '.join(tags))
        elif command == "exit":
            print("Program closed.")
            sys.exit(0)
        else:
            print("Invalid command, try again.")


if __name__ == "__main__":
    quote_finder()
# name: Steve Martin    name: Albert Einstein
