from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .forms import AlterCommentForm, NewCommentForm
from utils.decorators import comment_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_comment, check_work_space


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

    link = reverse("work_space:space_view", args=(space.pk,))
    return redirect(link)


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):
    """Deletes added comment"""

    # Check comment and if user has right to its deletion
    comment = check_comment(comment_id, request.user)

    # Delete comment from the db
    comment.delete()

    link = reverse("work_space:space_view", args=(comment.work_space.pk,))
    return redirect(link)


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

    link = reverse("work_space:space_view", args=(comment.work_space.pk,))
    return redirect(link)
