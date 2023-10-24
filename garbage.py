from django.core.exceptions import ValidationError


def validate_file_extension(value):
    print(value.file.content_type)
    if value.file.content_type != "application/pdf":
        raise ValidationError(u'Error message')
    
