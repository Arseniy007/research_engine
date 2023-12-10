def format_authors_apa(author_field: str) -> str:
    """Format author(s) like this: 'Donn J., Marx K.'"""
    authors: list = author_field.split(", ")
    number_of_authors = len(authors)
    first_author = format_one_author_apa(authors[0])

    if number_of_authors == 1:
        # Return "Donn, J."
        return first_author
    
    second_author = format_one_author_apa(authors[1])
    if number_of_authors == 2:
        # Return "Donn, J. & Tolkin, J.R."
        return f"{first_author} & {second_author}"
    
    if number_of_authors == 3:
        # Return "Donn, J., Tolkin, J.R. & Rowling J.K."
        third_author = format_authors_apa(authors[2])
        return f"{first_author}, {second_author} & {third_author}"

    # If there are more thean 3 authors
    other_authors: list = []
    for i in range(2, number_of_authors):
        other_author = format_one_author_apa(authors[i])
        other_authors.append(other_author)

    # Get last author and delete it from other_authors array
    last_author = other_authors.pop(-1)

    # Return "Donn J., Tolkien J.R., & Rowling J. K."
    other_authors = ", ".join(sorted(other_authors))
    return f"{first_author}, {second_author}, {other_authors} & {last_author}"


def format_one_author_apa(author: str) -> str:
    """Format one author like this: 'Donn J.'"""
    names: list = author.split()
    last_name = names[0]
    names_length = len(names)

    # Return "Homer"
    if names_length == 1:
        return last_name
    
    # Return "Donn J."
    first_name = names[1]
    if names_length == 2:
        return f"{last_name} {first_name[0]}."
    
    # Return "Tolkin J.R."
    second_name = names[2]
    return f"{last_name}, {first_name[0]}. {second_name[0]}."


def format_authors_mla(author_field: str) -> str:
    """Format author(s) like this: 'Donn, John and Marx, Karl'"""
    authors: list = author_field.split(", ")
    number_of_authors = len(authors)
    first_author = format_one_author_mla(authors[0])

    if number_of_authors == 1:
        # Return "Donn, John"
        return first_author
    elif number_of_authors == 2:
        # Return "Donn, John and Marx, Karl"
        second_author = format_one_author_mla(authors[1])
        return f"{first_author} and {second_author}"
    
    # If there are more then 2 authors:
    return f"{first_author}, et. al."


def format_one_author_mla(author: str) -> str:
    """Format one author like this: 'Donn, John'"""
    names: list = author.split()
    last_name = names[0]
    names_length = len(names)

    # Return "Homer"
    if names_length == 1:
        return last_name

    # Return "Donn, John"
    first_name = names[1]
    if names_length == 2:
        return f"{last_name}, {first_name}"

    # Return "Tolkien, John Ronald"
    second_name = names[2]
    return f"{last_name}, {first_name} {second_name}"
