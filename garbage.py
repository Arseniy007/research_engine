from django.core.exceptions import ValidationError


def validate_file_extension(value):
    print(value.file.content_type)
    if value.file.content_type != "application/pdf":
        raise ValidationError(u'Error message')
    


    """
    def __str__(self):
        return f"uploads/papers/{str(self.file)}"
    """

    """
    def file_link(self):
        
        return format_html("<a href='%s'>download</a>" % (f"file/uploads/papers/{self.file.url}",))
    
    file_link.allow_tags = True
    """



"""

@login_required(redirect_field_name=None)
def pdf_view(request, file_path):

    try:
        return FileResponse(open(file_path, 'rb'), contenttype="application/ms-word")
    except FileNotFoundError:
        raise Http404()




@login_required(redirect_field_name=None)
def word_view(request, file_path):
    pass

"""


"""

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

"""


"""

def delete_files(paper_id, user):

    # TODO

    paper = check_paper(paper_id, user)

    files_directory_location = paper.get_path()

    remove(files_directory_location)

 """


"""


from django.http import FileResponse

from . verification import check_file


def display_file(user, file_id):

    file = check_file(file_id, user)

    return FileResponse(open(file.get_path(), "rb"))


"""



"""





































"""