from .dates import validate_date
from .forms import BookForm, ArticleForm, ChapterForm, WebpageForm
from .models import Article, Book, Chapter, Source, Webpage, Endnote
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla
from user_management.models import User
from utils.verification import check_link
from work_space.models import WorkSpace


def clean_text_data(data: str, url=False):
    """Cleans given str-field"""
    cleaned_data = data.strip(""".,'" """)
    if url:
        return cleaned_data
    return cleaned_data.capitalize()


def clean_author_data(data, chapter_author=False) -> str | bool:
    """Get, clean and validate all author-related form-field"""
    try:
        # Get number of authors
        if chapter_author:
            number_of_authors = int(data.get("number_of_chapter_authors"))
        else:
            number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        return False
    
    authors: list = []
    for i in range(number_of_authors):
        if chapter_author:
            last_name = data.get(f"chapter_last_name_{i}")
            first_name = data.get(f"chapter_first_name_{i}")
            second_name = data.get(f"chapter_second_name_{i}")
        else:
            last_name = data.get(f"last_name_{i}")
            first_name = data.get(f"first_name_{i}")
            second_name = data.get(f"second_name_{i}")

        # Return if last_name field was somehow left blank
        if not last_name:
            return False

        last_name = clean_text_data(last_name)
        if not first_name:
            # If there is only last name
            author = last_name
        else:
            first_name = clean_text_data(first_name)
            if second_name:
                second_name = clean_text_data(second_name)
                # Case with multiple names
                author = f"{last_name} {first_name} {second_name}"
            else:
                # Case without second names
                author = f"{last_name} {first_name}"
            
        authors.append(author)
    # Make str from authors list, separating authors by comma
    return ", ".join(authors)


def save_endnotes(source: Source):
    """Creates and saves new Endnote obj for given source"""
    endnotes = Endnote(source=source, apa=quote_source_apa(source), mla=quote_source_mla(source))
    return endnotes.save()


def create_source(user: User, space: WorkSpace, form, author, chapter_author=None):
    """Get future source type and call right func"""
    match form:
        case BookForm():
            return create_book_obj(user, space, form, author)
        case ArticleForm():
            return create_article_obj(user, space, form, author)
        case ChapterForm():
            return create_chapter_obj(user, space, form, author, chapter_author)
        case WebpageForm():
            return create_webpage_obj(user, space, form, author)


def create_book_obj(user: User, space: WorkSpace, form: BookForm, author):
    """Validate Bookform and create Book obj"""

    # Iterate through all fields and clean its data
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info

    # Create and save new Book obj
    new_book = Book(work_space=space, user=user, title=data["title"], author=author, year=data["year"], 
                    publishing_house=data["publishing_house"])
    
    new_book.save()
    # Create new Endnote obj with Foreign key to this Book obj
    return save_endnotes(new_book)


def create_article_obj(user: User, space: WorkSpace, form: ArticleForm, author: str):
    """Validate Articleform and create Article obj"""

    # Iterate through all fields and clean its data
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info

    # Create and save new Article obj
    new_article = Article(work_space=space, user=user, title=data["article_title"], author=author, year=data["year"], 
                            journal_title=data["journal_title"], volume=data["volume"], 
                            issue=data["issue"], pages=data["pages"], link_to_journal=data["link_to_journal"])
    new_article.save()
    # Create new Endnote obj with Foreign key to this Article obj
    return save_endnotes(new_article)


def create_chapter_obj(user: User, space: WorkSpace, form: ChapterForm, book_author: str, chapter_author: str):
    """Validate Chapterform and create Chapter obj"""

    # Iterate through all fields and clean its data
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info
    
    # Create and save new Chapter obj
    new_chapter = Chapter(work_space=space, user=user, author=chapter_author, 
                            title=data["chapter_title"], book_title=data["book_title"], book_author=book_author,
                            publishing_house = data["publishing_house"], year=data["year"], edition = data["edition"], pages=data["pages"])
    new_chapter.save()
    # Create new Endnote obj with Foreign key to this Chapter obj
    return save_endnotes(new_chapter)


def create_webpage_obj(user: User, space: WorkSpace, form: WebpageForm, author: str | None):
    """Validate Webpageform and create Webpage obj"""

    # Iterate through all fields and clean its data
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            if field == "page_url":
                info = clean_text_data(info, url=True)
            info = clean_text_data(info)
        data[field] = info

    if not author:
        author = "No author"

    # Checks date and if a given page url is indeed a link and gets you to a real webpage
    page_url, date = data["page_url"], data["date"]
    if not check_link(page_url) or not validate_date(date):
        # TODO
        pass

    # Create and save new Webpage obj
    new_webpage = Webpage(work_space=space, user=user, title=data["page_title"], author=author, 
                            website_title=data["website_title"], page_url=page_url, date=date)
    new_webpage.save()
    # Create new Endnote obj with Foreign key to this Webpage obj
    return save_endnotes(new_webpage)
