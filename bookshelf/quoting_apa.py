from .models import Source, Article, Book, Chapter, Website


def format_authors_apa(author_field: str) -> str:
    """Format author(s) like this: 'Donn J., Marx K.'"""

    authors = author_field.split(", ")
    authors_name = []

    # Interate through every aurhor
    for one in authors:
        name = one.split()
        last_name = name[0]
        # Get initials
        initials = ""
        # Iterate through first and second names
        for i in range(1, len(name)):
            initials += f"{name[i][0]}."
            
        authors_name.append(f"{last_name} {initials}")
    return ", ".join(authors_name)


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
    return f"{last_name} {first_name[0]}. {second_name[0]}."
    

def quote_source_apa(source: Source):
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


def quote_book_apa(book: Book):
    """Create apa endnote for given book"""

    author = format_authors_apa(book.author)
    return f"{author} ({book.year}). {book.title}. {book.publishing_house}."


def quote_article_apa(article: Article):
    "Create apa endnote for given article"

    author = format_authors_apa(article.author)
    return f"""{author} ({article.year}). "{article.title}" {article.journal_title}, {article.volume}({article.issue}), {article.pages}."""


def quote_chapter_apa(chapter: Chapter):
    """Create apa endnote for given chapter"""
    # TODO
    return "Chapter apa"


def quote_website_apa(website: Website):
    """Create apa endnote for given website"""
    # TODO
    return "Website apa"
