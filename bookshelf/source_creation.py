from typing import Callable
from django import forms
from user_management.models import User
from utils.data_cleaning import clean_source_form_fields
from work_space.models import WorkSpace
from .source_citation import create_source_reference
from .forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from .models import Article, Book, Chapter, Webpage


def create_source(user: User, space: WorkSpace, form: forms.Form, author: str, chapter_author=None) -> Callable | None:
    """Get future source type and call right func"""

    # Iterate through all fields and clean its data
    cleaned_data: dict = clean_source_form_fields(form)

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


def create_book_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str) -> int:
    """Validate Book form, create Book obj and return its id"""

    # Create and save new Book obj
    new_book = Book(work_space=space, user=user, author=author, title=cleaned_data["title"], 
                    year=cleaned_data["year"], publishing_house=cleaned_data["publishing_house"])
    new_book.save()
    # Create new Reference obj with Foreign key to this Book obj
    create_source_reference(new_book)
    return new_book.pk


def create_article_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str) -> int:
    """Validate Article form, create Article obj and return its id"""

    # Create and save new Article obj
    new_article = Article(work_space=space, user=user, author=author, title=cleaned_data["article_title"], 
                          year=cleaned_data["year"], journal_title=cleaned_data["journal_title"], 
                          volume=cleaned_data["volume"], issue=cleaned_data["issue"], 
                          pages=cleaned_data["pages"], link_to_journal=cleaned_data["link_to_journal"])
    new_article.save()
    # Create new Reference obj with Foreign key to this Article obj
    create_source_reference(new_article)
    return new_article.pk


def create_chapter_obj(user: User, space: WorkSpace, cleaned_data: dict, book_author: str, chapter_author: str) -> int:
    """Validate Chapter form, create Chapter obj and return its id"""

    # Create and save new Chapter obj
    new_chapter = Chapter(work_space=space, user=user, author=chapter_author, book_author=book_author, 
                          title=cleaned_data["chapter_title"], book_title=cleaned_data["book_title"],
                          publishing_house = cleaned_data["publishing_house"], year=cleaned_data["year"],
                          edition = cleaned_data["edition"], pages=cleaned_data["pages"])
    new_chapter.save()
    # Create new Reference obj with Foreign key to this Chapter obj
    create_source_reference(new_chapter)
    return new_chapter.pk


def create_webpage_obj(user: User, space: WorkSpace, cleaned_data: dict, author: str | None) -> int:
    """Validate Webpage form, create Webpage obj and return its id"""

    if not author:
        author = "No author"

    # Checks date and if a given page url is indeed a link and gets you to a real webpage
    link, date = cleaned_data["link"], cleaned_data["date"]

    # Create and save new Webpage obj
    new_webpage = Webpage(work_space=space, user=user, author=author, 
                          link=link, date=date, title=cleaned_data["title"],
                          website_title=cleaned_data["website_title"])
    new_webpage.save()
    # Create new Reference obj with Foreign key to this Webpage obj
    create_source_reference(new_webpage)
    return new_webpage.pk
