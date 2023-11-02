from bookshelf.models import Book



def quote_book_apa(book):

    author = book.author.all()[0]

    return f"{author.last_name} {author.initials} ({book.year}). \x1B[3m{book.title}\x1B[0m. {book.publishing_house}"
