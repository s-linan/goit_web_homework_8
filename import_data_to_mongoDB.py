from connect import connect_to_db
from models import Author, Quote
import json


def load_data_from_json(file_path, model):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in data:
            obj = model(**i)
            obj.save()


if __name__ == "__main__":
    connect_to_db()
    load_data_from_json('authors.json', Author)
    load_data_from_json('quotes.json', Quote)
