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