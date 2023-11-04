from django.http import Http404

from .verification import check_work_space, check_book, check_paper


def space_ownership_required(func: function):
    """Checks if current user is owner of the work_space"""
    def wrapper(request, space_id):

        space = check_work_space(space_id, request.user)
        if space.owner != request.user:
            raise Http404
        
        return func(request, space_id)
    return wrapper


def book_ownership_required(func: function):
    """Checks if current user added this book"""
    def wrapper(request, book_id):

        book = check_book(book_id, request.user)
        if book.user != request.user:
            raise Http404
        
        return func(request, book_id)
    return wrapper


def authorship_required(func: function):
    """Checks if current user is author of the paper"""
    def wrapper(request, paper_id):
        
        paper = check_paper(paper_id, request.user)
        if paper.user != request.user:
            raise Http404
        
        return func(request, paper_id)
    return wrapper
