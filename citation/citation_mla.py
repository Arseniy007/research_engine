from .author_formatting import format_authors_mla
from .dates import format_date


def make_book_endnote_mla(book: dict) -> str:
    """Create mla endnote for given book"""
    author = format_authors_mla(book["author"])
    return f"{author}. {book['title']}. {book['publishing_house']}, {book['year']}."


def make_article_endnote_mla(article: dict) -> str:
    """Create mla endnote for given article"""
    author = format_authors_mla(article["author"])
    result: str = (
        f'{author}. "{article["title"]}". {article["journal_title"]}, vol. {article["volume"]}, '
        f'no. {article["issue"]}, {article["year"]}, pp. {article["pages"]}.'
    )
    return result


def make_chapter_endnote_mla(chapter: dict) -> str:
    """Create mla endnote for given chapter"""
    book_author = format_authors_mla(chapter["book_author"])
    chapter_author = format_authors_mla(chapter["author"])
    result: str = (
        f'{chapter_author}. "{chapter["title"]}." {chapter["book_title"]}, edited by {book_author}. '
        f'{chapter["publishing_house"]}, {chapter["year"]}, pp. {chapter["pages"]}.'
    )
    return result


def make_webpage_endnote_mla(webpage: dict) -> str:
    """Create mla endnote for given webpage"""
    date = format_date(str(webpage["date"]), "mla")
    if webpage["author"] == "No author":
        return f'"{webpage["title"]}" {webpage["website_title"]}, {date}, {webpage["link"]}.'

    author = format_authors_mla(webpage["author"])
    return f'{author}. "{webpage["title"]}" {webpage["website_title"]}, {date}, {webpage["link"]}.'
