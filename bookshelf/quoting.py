from bookshelf.models import Book


def quote_book_apa(book):
    """Makes qoute following APA standarts"""

    # TODO
    # Check (maybe using re module) unwnted spaces/dots/etc.

    authors = book.author.split(",")
    authors_name = []

    for one in authors:

        name = one.split()
        last_name = name[0]
        initials = ""

        for i in range(1, len(name)):
            initials += f"{name[i][0]}."
            
        authors_name.append(f"{last_name} {initials}")
            
    if len(authors_name) == 1:
        author = authors_name[0]
    else:
        author = ", ".join(authors_name)

    return f"{author} ({book.year}). {book.title}. {book.publishing_house}"


def quote_book_mla(book):
    """Makes qoute following MLA standarts"""
    # TODO

    pass
