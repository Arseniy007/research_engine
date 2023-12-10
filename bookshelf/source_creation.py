from typing import Callable
from django import forms
from .endnotes import save_endnotes
from .forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from .models import Article, Book, Chapter, Webpage
from quoting.data_cleaning import clean_text_data
from quoting.dates import validate_date
from user_management.models import User
from utils.verification import check_link
from work_space.models import WorkSpace


def create_source(user: User, space: WorkSpace, form: forms.Form, author: str, chapter_author=None) -> Callable | None:
    """Get future source type and call right func"""

    # Iterate through all fields and clean its data
    cleaned_data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        cleaned_data[field] = info

    match form:
        case BookForm():
            return create_book_obj(user, space, cleaned_data, author)
        case ArticleForm():
            return create_article_obj(user, space, cleaned_data, author)
        case ChapterForm():
            return create_chapter_obj(user, space, cleaned_data, author, chapter_author)
        case WebpageForm():
            return create_webpage_obj(user, space, cleaned_data, author)
        case _:
            return None


def create_book_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str):
    """Validate Bookform and create Book obj"""

    # Create and save new Book obj
    new_book = Book(work_space=space, user=user, author=author, title=cleaned_data["title"], 
                    year=cleaned_data["year"], publishing_house=cleaned_data["publishing_house"])
    new_book.save()
    # Create new Endnote obj with Foreign key to this Book obj
    return save_endnotes(new_book)


def create_article_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str):
    """Validate Articleform and create Article obj"""

    # Create and save new Article obj
    new_article = Article(work_space=space, user=user, author=author, title=cleaned_data["article_title"], 
                          year=cleaned_data["year"], journal_title=cleaned_data["journal_title"], 
                          volume=cleaned_data["volume"], issue=cleaned_data["issue"], 
                          pages=cleaned_data["pages"], link_to_journal=cleaned_data["link_to_journal"])
    new_article.save()
    # Create new Endnote obj with Foreign key to this Article obj
    return save_endnotes(new_article)


def create_chapter_obj(user: User, space: WorkSpace, cleaned_data: dict, book_author: str, chapter_author: str):
    """Validate Chapterform and create Chapter obj"""
    
    # Create and save new Chapter obj
    new_chapter = Chapter(work_space=space, user=user, author=chapter_author, book_author=book_author, 
                          title=cleaned_data["chapter_title"], book_title=cleaned_data["book_title"],
                          publishing_house = cleaned_data["publishing_house"], year=cleaned_data["year"],
                          edition = cleaned_data["edition"], pages=cleaned_data["pages"])
    new_chapter.save()
    # Create new Endnote obj with Foreign key to this Chapter obj
    return save_endnotes(new_chapter)


def create_webpage_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str | None):
    """Validate Webpageform and create Webpage obj"""

    if not author:
        author = "No author"

    # Checks date and if a given page url is indeed a link and gets you to a real webpage
    page_url, date = cleaned_data["page_url"], cleaned_data["date"]
    if not check_link(page_url) or not validate_date(date):
        # TODO
        pass

    # Create and save new Webpage obj
    new_webpage = Webpage(work_space=space, user=user, author=author, 
                          page_url=page_url, date=date, title=cleaned_data["page_title"],
                          website_title=cleaned_data["website_title"])
    new_webpage.save()
    # Create new Endnote obj with Foreign key to this Webpage obj
    return save_endnotes(new_webpage)
