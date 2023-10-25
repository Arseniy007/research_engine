from .check_paper import check_paper, check_file
from django.http import FileResponse

def handle_file_2(user_id, file_id):

    file = check_file(user_id, file_id)

    if not file:
        # TODO
        pass


    location = file.get_path()

    opened_file = open(location, "rb")

    return FileResponse(opened_file)