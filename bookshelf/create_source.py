#### Here should be something
from .forms import BookForm, ArticleForm, ChapterForm, WebsiteForm
from .models import Article, Book, Chapter, Source, Website, Endnote
from .quoting_apa import quote_source_apa
from .quoting_mla import quote_source_mla

from user_management.models import User
from work_space.models import WorkSpace


def clean_text_data(data: str):
    return data.strip(""".,'" """).capitalize()


def clean_author_data(data) -> str | bool:
    """Get, clean and validate all author-related form-field"""
    try:
        # Get number of authors
        number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        return False
    
    authors: list = []
    for i in range(number_of_authors):
        last_name = data.get(f"last_name_{i}")
        first_name = data.get(f"first_name_{i}")
        second_name = data.get(f"second_name_{i}")

        if not last_name:
            # TODO
            pass

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


def create_source(user: User, space: WorkSpace, form, author):
    """Get future source type and call right func"""
    match form:
        case BookForm():
            return create_book_obj(user, space, form, author)
        case ArticleForm():
            return create_article_obj(user, space, form, author)
        case ChapterForm():
            return create_chapter_obj(user, space, form, author)
        case WebsiteForm():
            return create_website_obj(user, space, form, author)


def create_book_obj(user: User, space: WorkSpace, form: BookForm, author):
    """Validate Bookform and create Book obj"""
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info

    new_book = Book(work_space=space, user=user, title=data["title"], author=author, year=data["year"], 
                    publishing_house=data["publishing_house"])
    
    new_book.save()
    return save_endnotes(new_book)


def create_article_obj(user: User, space: WorkSpace, form: ArticleForm, author):
    """Validate Articleform and create Article obj"""
    data: dict = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info

    new_article = Article(work_space=space, user=user, title=data["article_title"], author=author, year=data["year"], 
                            journal_title=data["journal_title"], volume=data["volume"], 
                            issue=data["issue"], pages=data["pages"], link_to_journal=data["link_to_journal"])
    
    new_article.save()
    return save_endnotes(new_article)





def create_chapter_obj(user: User, space: WorkSpace, form: ChapterForm, author):
    """Validate Chapterform and create Chapter obj"""

    data: dict = {}

    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info
    
    new_chapter = Chapter(work_space=space, user=user, title=data["book_title"], author=data["book_author"], 
                            chapter_title=data["chapter_title"], chapter_author=data["chapter_author"],
                            edition = data["edition"], pages=data["pages"], link=data["link"])
    
    new_chapter.save()
    return save_endnotes(new_chapter)



 


def create_website_obj(user: User, space: WorkSpace, form: WebsiteForm, author):
    """Validate Websiteform and create Website obj"""

    data: dict = {}

    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        data[field] = info

    new_website = Website(work_space=space, user=user, title=data["page_title"], author = data["page_author"], 
                            website_title=data["website_title"], page_url=data["page_url"], date=data["date"])
    
    new_website.save()
    return save_endnotes(new_website)
