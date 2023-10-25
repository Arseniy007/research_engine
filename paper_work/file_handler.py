from django.http import FileResponse, Http404

from . verification import check_file


def display_file(user, file_id):

    file = check_file(file_id, user)

    if not file:
        raise Http404

    return FileResponse(open(file.get_path(), "rb"))


def delete_files():
    """Deletes all files in the system related to the deleted paper"""
    # TODO
    pass
