from models import Authors, Quotes
import connect
import json

with open("./test_spyder/authors.json", "rb") as f:
    data_authors = json.load(f)
for i in data_authors:
    authors = Authors.from_json(json.dumps(i))
    authors.save()

with open("./test_spyder/quotes.json", "rb") as f:
    data_quotes = json.load(f)
for i in data_quotes:
    for j in i.items():
        if j[0]=="author":
            try:
                i["author"]=Authors.objects.get(fullname=j[1])
            except Authors.DoesNotExist:
                print(f"Author '{j[1]}' does not exist.")

for i in data_quotes:
    quotes = Quotes(**i)
    quotes.save()
