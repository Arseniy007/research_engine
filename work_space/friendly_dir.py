import os
import shutil
from work_space.models import WorkSpace
from bookshelf.source_citation import get_source_reference


def create_friendly_space_directory(work_space: WorkSpace) -> str | bool:
    """Creates user-friendly directory for future zip-archiving and downloading"""

    # Get all sources, papers, comments, notes and links in given work space
    sources, papers = work_space.sources.all(), work_space.papers.all()
    comments, notes, links = work_space.comments.all(), work_space.notes.all(), work_space.links.all()

    if not sources and not papers:
        # In case work space is empty
        return False

    # Get all work space users
    owner, guests = work_space.owner, work_space.guests.all()
    if guests:
        users = list(guests)
        users.append(owner)
    else:
        users = [owner]

    # TODO Not all users upload files

    # Create new empty directory
    work_space.create_friendly_dir()
    original_path = work_space.get_friendly_path()
    root_path = os.path.join(original_path, work_space.title)

    if sources:
        # Create new "books" dir
        create_friendly_sources_dir(sources, root_path)

    if papers:
        # Create new "papers" dir
       create_friendly_papers_dir(papers, users, root_path)

    if notes:
        # Create new "notes" txt-file
        create_friendly_notes_dir(notes, users, root_path)
                    
    if comments:
        # Create new "comments" txt-file
        create_friendly_comments_file(comments, root_path)

    if links:
        # Create new "links" txt-file
        create_friendly_links_file(links, root_path)

    # Return path to the whole dir
    return original_path


def create_friendly_sources_directory(work_space: WorkSpace) -> str | bool:
    """Creates user-friendly directory with all space-related sources for future zip-archiving and downloading"""

    # Get all sources in given work space
    sources = work_space.sources.all()
    if not sources:
        return False
    
    # Create new empty directory
    work_space.create_friendly_dir()
    original_path = work_space.get_friendly_path()
    root_path = os.path.join(original_path, "My sources")

    # Create new "books" dir
    create_friendly_sources_dir(sources, root_path)

    # Return path to the whole dir
    return original_path


def create_friendly_sources_dir(sources, root_path: str) -> None:
    """Create new "books" dir with all space-related sources inside"""
    
    books_root = os.path.join(root_path, "books")
    os.makedirs(books_root, exist_ok=True)

    # Get, quote and sort alphabetically all sources
    sources_apa = sorted([get_source_reference(source).endnote_apa for source in sources])
    sources_mla = sorted([get_source_reference(source).endnote_mla for source in sources])

    # Get paths to new .txt files
    apa_file_path = os.path.join(books_root, "books_apa.txt")
    mla_file_path = os.path.join(books_root, "books_mla.txt")

    # Create two new .txt files
    with open(apa_file_path, "w") as apa_file, open(mla_file_path, "w") as mla_file:
        source_counter = 1
        for i in range(len(sources)):
            # Write sources arrays into both files
            apa_file.write(f"{source_counter}. {sources_apa[i]}\n\n")
            mla_file.write(f"{source_counter}. {sources_mla[i]}\n\n")
            source_counter += 1

    # Get array with only sources which files were uploaded
    sources_with_files = [source for source in sources if source.has_file()]

    if any(sources_with_files):
        # Create new "sources-files" dir
        sources_files_root = os.path.join(books_root, "files")
        os.makedirs(sources_files_root, exist_ok=True)

        for source in sources_with_files:
            # Copy original source file into new "sources-file" dir
            destination = os.path.join(sources_files_root, source.file.file_name())
            original_file = source.get_path_to_file()
            shutil.copyfile(original_file, destination)

    # Get array with only sources with quotes
    sources_with_quotes = [source for source in sources if source.quotes.all()]

    if any(sources_with_quotes):
        # Get paths to new .txt file
        quotes_file = os.path.join(books_root, "quotes.txt")

        # Create file and write in all quotes
        with open(quotes_file, "w") as file:
            for source in sources_with_quotes:
                # Write every source title
                file.write(f"\t{source}\n\n\n")
                source_quotes = source.quotes.all()
                # Write all its quotes
                for quote in source_quotes:
                    file.write(f"{quote}\n\n")
                file.write("\n\n")


def create_friendly_papers_dir(papers, authors: list, root_path: str) -> None:
    """Create new "papers" dir with all space-related papers inside"""
    
    papers_root = os.path.join(root_path, "papers")
    os.makedirs(papers_root, exist_ok=True)

    # Get all users    
    for author in authors:
        if len(authors) == 1:
             # Don't create author dir if there is only one user
            author_root = papers_root
        else:
            # Create new "user" dirs inside "papers" dir if there are multiple users
            author_name = f"{author.last_name} {author.first_name}"
            author_root = os.path.join(papers_root, author_name)
            os.makedirs(author_root, exist_ok=True)

        # Get all user papers
        author_papers = [paper for paper in papers if paper.user == author]
        for author_paper in author_papers:
            # Create new "paper" dirs inside "user" dir
            path_to_paper = os.path.join(author_root, author_paper.title)
            os.makedirs(path_to_paper, exist_ok=True)

            # Get all paper-related files
            files = author_paper.files.all()
            for file in files:
                # Create new "paper-file" dirs inside "paper" dir
                path_to_paper_file = os.path.join(path_to_paper, file.get_saving_time())
                os.makedirs(path_to_paper_file, exist_ok=True)

                # Copy original paper file into new "paper-file" dir
                destination = os.path.join(path_to_paper_file, file.file_name())
                original_file = file.get_path_to_file()
                shutil.copyfile(original_file, destination)         


def create_friendly_notes_dir(notes, authors: list, root_path: str) -> None:
    """Create new "notes" txt file with all space-related notes inside"""

    notes_root = os.path.join(root_path, "notes")
    os.makedirs(notes_root, exist_ok=True)

    # Get all users
    for author in authors:
        if len(authors) == 1:
            # Don't create author dir if there is only one user
            author_root = notes_root
        else:
            # Create new "user" dirs inside "notes" dir if there are multiple users
            author_name = f"{author.last_name} {author.first_name}"
            author_root = os.path.join(notes_root, author_name)
            os.makedirs(author_root, exist_ok=True)

        # Get all user notes
        author_notes = [note for note in notes if note.user == author]
        for author_note in author_notes:
            # Get path to new note .txt file
            path_to_note = os.path.join(author_root, f"{author_note.title}.txt")

            # Create file and write in note text
            with open(path_to_note, "w") as note_file:
                note_file.write(author_note.text)


def create_friendly_comments_file(comments, root_path: str) -> None:
    """Create new "comments" txt file with all space-related comments inside"""

    # Get path to new comments.txt file
    comments_file_path = os.path.join(root_path, "comments.txt")

    # Create file and write in all comments
    with open(comments_file_path, "w") as comment_file:
        for comment in comments:
            comment_file.write(f"{comment}\n\n")


def create_friendly_links_file(links, root_path: str) -> None:
    """Create new "links" txt file with all space-related links inside"""
    
    # Get path to new links.txt file
    links_file_path = os.path.join(root_path, "links.txt")

    # Create file and write in all links
    with open(links_file_path, "w") as link_file:
        for link in links:
            link_file.write(f"{link}:\n{link.url}\n\n")
