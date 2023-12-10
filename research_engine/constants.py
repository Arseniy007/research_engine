from django.urls import reverse
from .settings import MEDIA_ROOT


ERROR_PAGE = reverse("website:error_page")

FRIENDLY_TMP_ROOT = f'{MEDIA_ROOT}/friendly_dirs'

ACCEPTED_UPLOAD_FORMATS = ".pdf, .docx"

SAVING_TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
