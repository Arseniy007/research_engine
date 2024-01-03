from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import AlterCommentForm, AlterLinkForm, AlterNoteForm, NewCommentForm, NewLinkForm, NewNoteForm
from utils.decorators import comment_authorship_required, link_ownership_required, note_authorship_required, post_request_required
from utils.messages import display_error_message
from utils.verification import check_comment, check_note, check_space_link, check_work_space


@post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):
    """Leaves comment in given workspace"""
    
    form = NewCommentForm(request.POST)

    if form and form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        new_comment = form.save_comment(space, request.user)
        return JsonResponse({"status": "ok", "comment": model_to_dict(new_comment)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):
    """Alter comment text"""

    form = AlterCommentForm(request.POST)
    comment = check_comment(comment_id, request.user)

    if form and form.is_valid():
        altered_comment = form.save_altered_comment(comment)
        return JsonResponse({"status": "ok", "altered_comment": model_to_dict(altered_comment)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(comment.work_space.pk,))})


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):
    """Deletes added comment"""

    # Check comment and delete it from the db
    comment = check_comment(comment_id, request.user)
    comment.delete()
    return JsonResponse({"status": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def leave_note(request, space_id):
    """Leaves note in given workspace"""

    form = NewNoteForm(request.POST)

    if form and form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        new_note = form.save_note(space, request.user)
        return JsonResponse({"status": "ok", "new_note": model_to_dict(new_note)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@post_request_required
@note_authorship_required
@login_required(redirect_field_name=None)
def alter_note(request, note_id):
    """Alter note text"""
    
    form = AlterNoteForm(request.POST)
    note = check_note(note_id, request.user)

    if form and form.is_valid():
        altered_note = form.save_altered_note(note)
        return JsonResponse({"status": "ok", "altered_note": model_to_dict(altered_note)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(note.work_space.pk,))})


@note_authorship_required
@login_required(redirect_field_name=None)
def delete_note(request, note_id):
    """Deletes added note"""

    # Check note and delete it from the db
    note = check_note(note_id, request.user)
    note.delete()
    return JsonResponse({"status": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def add_link(request, space_id):
    """Add link to given workspace"""

    form = NewLinkForm(request.POST)

    if form and form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        new_link = form.save_link(space, request.user)
        return JsonResponse({"status": "ok", "link_name": new_link.name, "url": model_to_dict(new_link)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(space_id,))})


@post_request_required
@link_ownership_required
@login_required(redirect_field_name=None)
def alter_link(request, link_id):
    """Alter link name or url"""

    form = AlterLinkForm(request.POST)
    link = check_space_link(link_id, request.user)

    if form and form.is_valid():
        altered_link = form.save_altered_link(link)
        return JsonResponse({"status": "ok", "altered_link": model_to_dict(altered_link)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("work_space:space_view", args=(link.work_space.pk,))})


@link_ownership_required
@login_required(redirect_field_name=None)
def delete_link(request, link_id):
    """Deletes added link"""
    
    # Check link and delete if from the db
    link = check_space_link(link_id, request.user)
    link.delete()
    return JsonResponse({"status": "ok"})


@login_required(redirect_field_name=None)
def render_author_form_fields(request, author_number):

    return render(request, "bookshelf/author_fields.html", {"author_number": author_number})
