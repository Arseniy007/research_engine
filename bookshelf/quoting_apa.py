from .models import Source, Article, Book, Chapter, Website

# Author field:
# Lastname, firstname(, senond name) / Lastname, firstname(, senond name) /..

# Here comment how mla and apa differs from each other
# import re


def quote_source_apa(source: Source):
    """Get source type and call corresponding func"""

    source_type = source.cast()
    match source_type:
        case Book():
            return quote_book_apa(source.book)
        case Article():
            return quote_article_apa(source.article)
        case Chapter():
            return quote_chapter_apa(source.chapter)
        case Website():
            return quote_website_apa(source.website)
        case _:
            return None


def quote_book_apa(book: Book):
    """Makes qoute following APA standarts"""

    # TODO
    # Check (maybe using re module) unwanted spaces/dots/etc. - separate func!

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


def quote_article_apa(article: Article):
    # TODO

    authors = article.author.split(",")
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


    return f"""{author} ({article.year}). "{article.title}" {article.journal_title}, {article.volume}({article.issue}), {article.pages}."""



def quote_chapter_apa(chapter: Chapter):
    # TODO

    return "Chapter apa"



def quote_website_apa(website: Website):
    # TODO

    return "Website apa"

    pass

