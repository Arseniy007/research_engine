from django.contrib import messages


def display_success_message(request, message_text="Success!"):
    return messages.add_message(request, messages.SUCCESS, message_text)


def display_error_message(request, message_text="Error!"):
    return messages.add_message(request, messages.ERROR, message_text)


def display_info_message(request, message_text="Info!"):
    return messages.add_message(request, messages.INFO, message_text)
