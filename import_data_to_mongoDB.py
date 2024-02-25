from connect import connect_to_db
from models import Author, Quote
import json


def load_authors(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        data_of_authors = json.load(file)
        for author in data_of_authors:
            aut = Author(fullname=author.get("fullname"),
                         born_date=author.get("born_date"),
                         born_location=author.get("born_location"),
                         description=author.get("description"))
            aut.save()


def load_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data_quotes = json.load(file)
        for quote_data in data_quotes:
            author_name = quote_data.get('author')
            author = Author.objects.get(fullname=author_name) if author_name else None
            if author:
                quote = Quote(author=author,
                              tags=quote_data.get("tags"),
                              quote=quote_data.get("quote")
                              )
                quote.save()
            else:
                print(f"Author '{author_name}' not found.")


if __name__ == "__main__":
    connect_to_db()
    load_authors('authors.json')
    load_quotes('quotes.json')
