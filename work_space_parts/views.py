from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .forms import AlterCommentForm, AlterLinkForm, AlterNoteForm, NewCommentForm, NewLinkForm, NewNoteForm
from utils.decorators import comment_authorship_required, link_ownership_required, note_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_comment, check_note, check_space_link, check_work_space


@post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):
    """Leaves comment in given workspace"""

    form = NewCommentForm(request.POST)

    if form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        form.save_comment(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)

    return redirect(reverse("work_space:space_view", args=(space.pk,)))


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):
    """Deletes added comment"""

    # Check comment and if user has right to its deletion
    comment = check_comment(comment_id, request.user)

    # Delete comment from the db
    comment.delete()
    return redirect(reverse("work_space:space_view", args=(comment.work_space.pk,)))


@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):
    """Alter comment text"""

    form = AlterCommentForm(request.POST)

    if form.is_valid():
        comment = check_comment(comment_id, request.user)
        form.save_altered_comment(comment)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(comment.work_space.pk,)))


@login_required(redirect_field_name=None)
def leave_note(request, space_id):
    """Leaves note in given workspace"""

    form = NewNoteForm(request.POST)

    if form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        form.save_note(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(space.pk,)))


@note_authorship_required
@login_required(redirect_field_name=None)
def delete_note(request, note_id):
    """Deletes added note"""

    # Check note and if user has right to its deletion
    note = check_note(note_id, request.user)

    # Delete comment from the db
    note.delete()
    return redirect(reverse("work_space:space_view", args=(note.work_space.pk,)))


@note_authorship_required
@login_required(redirect_field_name=None)
def alter_note(request, note_id):
    """Alter note text"""
    
    form = AlterNoteForm(request.POST)

    if form.is_valid():
        note = check_note(note_id, request.user)
        form.save_altered_note(note)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(note.work_space.pk,)))


@login_required(redirect_field_name=None)
def add_link(request, space_id):
    """Add link to given workspace"""

    form = NewLinkForm(request.POST)

    if form.is_valid():
        # Create new Note obj
        space = check_work_space(space_id, request.user)
        form.save_link(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(space.pk,)))


@link_ownership_required
@login_required(redirect_field_name=None)
def delete_link(request, link_id):
    """Deletes added link"""
    
    link = check_space_link(link_id, request.user)

    # Delete link from the db
    link.delete()
    return redirect(reverse("work_space:space_view", args=(link.work_space.pk,)))


@link_ownership_required
@login_required(redirect_field_name=None)
def alter_link(request, link_id):
    """Alter link name or url"""

    form = AlterLinkForm(request.POST)

    if form.is_valid():
        link = check_space_link(link_id, request.user)
        form.save_altered_link(link)
        display_success_message(request)
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(link.work_space.pk,)))


# TODO: JSON!
