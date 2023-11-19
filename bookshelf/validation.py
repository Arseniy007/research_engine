def clean_text_data(data: str):
    return data.strip(""".,'" """)


def clean_author_data(data):
    """Get, clean and validate all author-related form-field"""
    try:
        number_of_authors = int(data.get("number_of_authors"))
    except ValueError:
        # TODO
        pass

    authors: list = []

    for i in range(number_of_authors):
        last_name = data.get(f"last_name_{i}")
        first_name = data.get(f"first_name_{i}")
        second_name = data.get(f"second_name_{i}")

        if not last_name:
            # TODO
            pass
        last_name = clean_text_data(last_name)
        
        if not first_name:
            author = last_name
        else:
            first_name = clean_text_data(first_name)
            if second_name:
                second_name = clean_text_data(second_name)
                author = f"{last_name} {first_name} {second_name}"
            else:
                author = f"{last_name} {first_name}"
            
        authors.append(author)
    return ", ".join(authors)
