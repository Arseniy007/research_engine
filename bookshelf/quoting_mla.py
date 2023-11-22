from typing import Callable
from .dates import format_date
from .models import Source, Article, Book, Chapter, Webpage


def format_authors_mla(author_field: str) -> str:
    """Format author(s) like this: 'Donn, John and Marx, Karl'"""
    authors: list = author_field.split(", ")
    number_of_authors = len(authors)
    first_author = format_one_author_mla(authors[0])

    if number_of_authors == 1:
        # Return "Donn, John"
        return first_author
    elif number_of_authors == 2:
        # Return "Donn, John and Marx, Karl"
        second_author = format_one_author_mla(authors[1])
        return f"{first_author} and {second_author}"
    
    # If there are more then 2 authors:
    return f"{first_author}, et. al."


def format_one_author_mla(author: str) -> str:
    """Format one author like this: 'Donn, John'"""
    names: list = author.split()
    last_name = names[0]
    names_length = len(names)

    # Return "Homer"
    if names_length == 1:
        return last_name

    # Return "Donn, John"
    first_name = names[1]
    if names_length == 2:
        return f"{last_name}, {first_name}"

    # Return "Tolkien, John Ronald"
    second_name = names[2]
    return f"{last_name}, {first_name} {second_name}"
    

def quote_source_mla(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: type(object) = source.cast()
    match source_type:
        case Book():
            return quote_book_mla(source.book)
        case Article():
            return quote_article_mla(source.article)
        case Chapter():
            return quote_chapter_mla(source.chapter)
        case Webpage():
            return quote_webpage_mla(source.webpage)
        case _:
            return None


def quote_book_mla(book: Book) -> str:
    """Create mla endnote for given book"""
    author = format_authors_mla(book.author)
    return f"{author} {book.title}. {book.publishing_house}, {book.year}."


def quote_article_mla(article: Article) -> str:
    """Create mla endnote for given article"""
    author = format_authors_mla(article.author)
    result: str = (
        f'{author} "{article.title}" {article.journal_title}, vol. {article.volume}, '
        f'no. {article.issue}, {article.year}, pp. {article.year}.'
    )
    return result


def quote_chapter_mla(chapter: Chapter) -> str:
    """Create mla endnote for given chapter"""
    book_author = format_authors_mla(chapter.book_author)
    chapter_author = format_authors_mla(chapter.author)
    result: str = (
        f'{chapter_author}. "{chapter.title}." {chapter.book_title}, edited by {book_author}. '
        f'{chapter.publishing_house}, {chapter.year}, pp. {chapter.pages}.'
    )
    return result


def quote_webpage_mla(webpage: Webpage) -> str:
    """Create mla endnote for given webpage"""
    date = format_date(webpage.date, "mla")
    if webpage.author == "No author":
        return f'"{webpage.title}" {webpage.website_title}, {date}, {webpage.page_url}.'
    
    author = format_authors_mla(webpage.author)
    return f'{author}. "{webpage.title}" {webpage.website_title}, {date}, {webpage.page_url}.'
