from .author_formatting import format_authors_apa
from .dates import format_date


def make_book_endnote_apa(book: dict) -> str:
    """Create apa endnote for given book"""
    author = format_authors_apa(book["author"])
    return f"{author} ({book['year']}). {book['title']}. {book['publishing_house']}."


def make_article_endnote_apa(article: dict) -> str:
    """Create apa endnote for given article"""
    author = format_authors_apa(article["author"])
    result: str = (
        f'{author} ({article["year"]}). "{article["title"]}" {article["journal_title"]}, '
        f'{article["volume"]}({article["issue"]}), {article["pages"]}.'
    )
    return result


def make_chapter_endnote_apa(chapter: dict) -> str:
    """Create apa endnote for given chapter"""
    book_author = format_authors_apa(chapter["book_author"])
    chapter_author = format_authors_apa(chapter["author"])
    result: str = (
        f"{chapter_author} ({chapter['year']}). {chapter['title']}. "
        f"In {book_author} (Eds.), {chapter['book_title']} "
        f"({chapter['edition']} ed., pp. {chapter['pages']}). {chapter['publishing_house']}."
    )
    return result


def make_webpage_endnote_apa(webpage: dict) -> str:
    """Create apa endnote for given webpage"""
    date = format_date(str(webpage["date"]), "apa")
    if webpage["author"] == "No author":
        return f"{webpage['title']}. ({date}). {webpage['website_title']}. {webpage['link']}"

    author = format_authors_apa(webpage["author"])
    return f"{author} ({date}). {webpage['title']}. {webpage['website_title']}. {webpage['link']}"
