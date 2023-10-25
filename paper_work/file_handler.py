from django.http import FileResponse

from . verification import check_file


def display_file(user_id, file_id):

    file = check_file(user_id, file_id)

    if not file:
        return False

    return FileResponse(open(file.get_path(), "rb"))



def delete_files():
    # TODO

    pass