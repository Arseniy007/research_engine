from typing import Callable
from .dates import format_date
from .models import Source, Article, Book, Chapter, Website


def format_authors_apa(author_field: str) -> str:
    """Format author(s) like this: 'Donn J., Marx K.'"""
    authors: list = author_field.split(", ")
    number_of_authors = len(authors)
    first_author = format_one_author_apa(authors[0])

    if number_of_authors == 1:
        # Return "Donn, J."
        return first_author
    
    second_author = format_one_author_apa(authors[1])
    if number_of_authors == 2:
        # Return "Donn, J. & Tolkin, J.R."
        return f"{first_author} & {second_author}"
    
    if number_of_authors == 3:
        # Return "Donn, J., Tolkin, J.R. & Rowling J.K."
        third_author = format_authors_apa(authors[2])
        return f"{first_author}, {second_author} & {third_author}"

    # If there are more thean 3 authors
    other_authors: list = []
    for i in range(2, number_of_authors):
        other_author = format_one_author_apa(authors[i])
        other_authors.append(other_author)

    # Get last author and delete it from other_authors array
    last_author = other_authors.pop(-1)

    # Return "Donn J., Tolkien J.R., & Rowling J. K."
    other_authors = ", ".join(sorted(other_authors))
    return f"{first_author}, {second_author}, {other_authors} & {last_author}"


def format_one_author_apa(author: str) -> str:
    """Format one author like this: 'Donn J.'"""
    names: list = author.split()
    last_name = names[0]
    names_length = len(names)

    # Return "Homer"
    if names_length == 1:
        return last_name
    
    # Return "Donn J."
    first_name = names[1]
    if names_length == 2:
        return f"{last_name} {first_name[0]}."
    
    # Return "Tolkin J.R."
    second_name = names[2]
    return f"{last_name}, {first_name[0]}. {second_name[0]}."


def quote_source_apa(source: Source) -> Callable | bool:
    """Get source type and call corresponding func"""

    source_type: type(object) = source.cast()
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


def quote_book_apa(book: Book) -> str:
    """Create apa endnote for given book"""
    author = format_authors_apa(book.author)
    return f"{author} ({book.year}). {book.title}. {book.publishing_house}."


def quote_article_apa(article: Article) -> str:
    "Create apa endnote for given article"
    author = format_authors_apa(article.author)
    result: str = (
        f'{author} ({article.year}). "{article.title}" {article.journal_title}, '
        f'{article.volume}({article.issue}), {article.pages}.'
    )
    return result


def quote_chapter_apa(chapter: Chapter) -> str:
    """Create apa endnote for given chapter"""
    book_author = format_authors_apa(chapter.book_author)
    chapter_author = format_authors_apa(chapter.author)
    result: str = (
        f"{chapter_author} ({chapter.year}). {chapter.title}. "
        f"In {book_author} (Eds.), {chapter.book_title} "
        f"({chapter.edition} ed., pp. {chapter.pages}). {chapter.publishing_house}."
    )
    return result


def quote_website_apa(website: Website) -> str:
    """Create apa endnote for given website"""
    # TODO

    if website.author == "No author":
        pass
    else:
        author = format_authors_apa(website.author)
    date = format_date(website.date, "apa")

    # 6. Del, c. I. (2020, June 29). How not to kill your houseplants, according to botanists.
    # Apartment therapy. Www.apartmenttherapy.com/houseplant-tips-botanists-36710191

    return f"{author} ({date}). {website.title}. {website.website_title}. {website.page_url}"
