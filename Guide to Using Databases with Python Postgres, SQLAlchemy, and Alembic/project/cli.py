from crud import Session
from models import Book

s = Session()

books = s.query(Book).all()

for book in books:
    price = input(f"Price for '{book.title}': $")
    book.price = price
    s.add(book)

s.commit()
s.close()