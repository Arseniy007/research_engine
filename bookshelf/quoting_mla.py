from .models import Source, Article, Book, Chapter, Website


def format_author_mla(author_field: str) -> str:
    pass


def quote_source_mla(source: Source):
    """Get source type and call corresponding func"""

    source_type = source.cast()
    match source_type:
        case Book():
            return quote_book_mla(source.book)
        case Article():
            return quote_article_mla(source.article)
        case Chapter():
            return quote_chapter_mla(source.chapter)
        case Website():
            return quote_website_mla(source.website)
        case _:
            return None


def quote_book_mla(source: Source):
    """Makes qoute following MLA standarts"""
    # TODO

    authors = source.author.split(", ")
    authors_name = []

    for one in authors:

        name = one.split()
        last_name = name[0]
        try:
            first_name = name[1]
        except IndexError:
            first_name = ""

        authors_name.append(f"{last_name}, {first_name}")
    
    author = authors_name[0]
    
    return f"{author}. {source.title}. {'PH'}, {source.year}."


def quote_article_mla(article: Article):

    authors = article.author.split(", ")
    authors_name = []

    for one in authors:

        name = one.split()
        last_name = name[0]
        try:
            first_name = name[1]
        except IndexError:
            first_name = ""

        authors_name.append(f"{last_name}, {first_name}")
    
    author = authors_name[0]

    return f"""{author}. "{article.title}" {article.journal_title}, vol. {article.volume}, no. {article.issue}, 
                {article.year}, pp. {article.year}."""


def quote_chapter_mla(chapter: Chapter):

    return "Chapter mla"


def quote_website_mla(website: Website):

    return "Website mla"
