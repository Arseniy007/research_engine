from django.forms import Form


def clean_text_data(data: str) -> str:
    """Cleans given str-field"""
    return data.strip(""".,'" """)


def clean_source_form_fields(form: Form) -> dict:
    """Clean all fields in submitted Source Form of any type"""
    cleaned_data = {}
    for field in form.fields:
        info = form.cleaned_data[field]
        if type(info) == str:
            info = clean_text_data(info)
        cleaned_data[field] = info
    return cleaned_data


def clean_author_data(data, chapter_author=False) -> str | bool:
    """Get, clean and validate all author-related form-field"""
    try:
        # Get number of authors
        if chapter_author:
            number_of_authors = int(data.get("number_of_chapter_authors"))
        else:
            number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        return False
    
    authors: list = []
    for i in range(number_of_authors):
        if chapter_author:
            last_name = data.get(f"chapter_last_name_{i}")
            first_name = data.get(f"chapter_first_name_{i}")
            second_name = data.get(f"chapter_second_name_{i}")
        else:
            last_name = data.get(f"last_name_{i}")
            first_name = data.get(f"first_name_{i}")
            second_name = data.get(f"second_name_{i}")

        # Return if last_name field was somehow left blank
        if not last_name:
            return False

        last_name = clean_text_data(last_name)
        if not first_name:
            # If there is only last name
            author = last_name
        else:
            first_name = clean_text_data(first_name)
            if second_name:
                second_name = clean_text_data(second_name)
                # Case with multiple names
                author = f"{last_name} {first_name} {second_name}"
            else:
                # Case without second names
                author = f"{last_name} {first_name}"
            
        authors.append(author)
    # Make str from authors list, separating authors by comma
    return ", ".join(authors)
