from django.core.exceptions import ValidationError

"""

def validate_file_extension(value):
    print(value.file.content_type)
    if value.file.content_type != "application/pdf":
        raise ValidationError(u'Error message')
"""


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
    words = text.split()
    header = "Lorem ipsum dolor sit amet"
    print(len(words) - len(header.split()))
    print(len(text) - len(header))

    print(text)
  

    
    

    #word_count = len(re.findall(r"\b\w+\b", text)) 

    #word_count = re.sub('<(.|\n)*?>','', text)

    #print(len(text))

    

    paragraphs = text.split("\n\n")

    num_of_word = len(paragraphs)

    for paragraph in paragraphs:

        if paragraph != "\n":

            words = len(paragraph.split())
            num_of_word += words

    num_of_word += len(paragraphs)
    
    
    print(num_of_word, "hf")
    print(len(text))
    #print(text.encode().decode('utf-8', 'ignore'))


    print(text)



    f"user_{instance.user.id}/paper_{instance.paper.pk}/{saving_date}/{filename}"

"""









"""
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/paper_<id>/<saving_date>/<filename>

    saving_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"user_{instance.paper.user.pk}/paper_{instance.paper.pk}/{saving_date}/{filename}"
"""

"""
def get_saving_time():

    return datetime.now().strftime(SAVING_TIME_FORMAT)

"""

"""
def ownership_required(function):

    def wrapper(user, space_id):
        
        space = check_work_space(space_id)

        if space.owner != user:
            raise Http404
        
        function(user, space_id)

    return wrapper

"""
























