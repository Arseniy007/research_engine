from typing import Callable
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from .verification import *


def post_request_required(func: Callable) -> Callable | HttpResponseBadRequest:
    """Checks type of request and allow only POST type"""
    def wrapper(request, *args, **kwargs):
        if request.method != "POST":
            return HttpResponseBadRequest("POST request required")
        return func(request, *args, **kwargs)
    return wrapper


def space_ownership_required(func: Callable) -> Callable | PermissionDenied:
    """Checks if current user is owner of the work_space"""
    def wrapper(request, space_id):
        space = check_work_space(space_id, request.user)
        if space.owner != request.user:
            raise PermissionDenied
        return func(request, space_id)
    return wrapper


def source_ownership_required(func: Callable) -> Callable | PermissionDenied:
    """Checks if current user added this source"""
    def wrapper(request, source_id):
        source = check_source(source_id, request.user)
        if source.user != request.user:
            raise PermissionDenied
        return func(request, source_id)
    return wrapper


def paper_authorship_required(func: Callable) -> Callable | PermissionDenied:
    """Checks if current user is author of the paper"""
    def wrapper(request, paper_id):
        paper = check_paper(paper_id, request.user)
        if paper.user != request.user:
            raise PermissionDenied 
        return func(request, paper_id)
    return wrapper


def quote_ownership_required(func: Callable) -> Callable | PermissionDenied:
    """Checks if current user added book to which given quote belongs"""
    def wrapper(request, quote_id):
        quote = check_quote(quote_id, request.user)
        if quote.source.user != request.user:
            raise PermissionDenied
        return func(request, quote_id)
    return wrapper
