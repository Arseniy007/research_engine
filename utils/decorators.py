from django.core.exceptions import PermissionDenied

from typing import Callable

from .verification import check_work_space, check_book, check_paper, check_quote, check_article, check_source


def space_ownership_required(func: Callable):
    """Checks if current user is owner of the work_space"""
    def wrapper(request, space_id):

        space = check_work_space(space_id, request.user)
        if space.owner != request.user:
            raise PermissionDenied
        
        return func(request, space_id)
    return wrapper



def source_ownership_required(func: Callable):
    """Checks if current user added this source"""
    def wrapper(*args, **kwargs):
        
        user = args[0].user
        source_id = kwargs[0]

        source = check_source(source_id, user)
        if source.user != args.user:
            raise PermissionDenied
    
        return func(*args, **kwargs)
    return wrapper



def article_ownership_required(func: Callable):
    """Checks if current user added this article"""
    def wrapper(request, article_id):

        article = check_article(article_id, request.user)
        if article.user != request.user:
            raise PermissionDenied
        
        return func(request, article_id)
    return wrapper


def book_ownership_required(func: Callable):
    """Checks if current user added this book"""
    def wrapper(request, book_id):

        book = check_book(book_id, request.user)
        if book.user != request.user:
            raise PermissionDenied
        
        return func(request, book_id)
    return wrapper


def quote_ownership_required(func: Callable):
    """Checks if current user added book to which given quote belongs"""
    def wrapper(request, quote_id):

        quote = check_quote(quote_id, request.user)
        if quote.book.user != request.user:
            raise PermissionDenied
        
        return func(request, quote_id)
    return wrapper


def paper_authorship_required(func: Callable):
    """Checks if current user is author of the paper"""
    def wrapper(request, paper_id):
        
        paper = check_paper(paper_id, request.user)
        if paper.user != request.user:
            raise PermissionDenied 
        
        return func(request, paper_id)
    return wrapper
