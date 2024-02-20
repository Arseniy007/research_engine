import os
import shutil
from bookshelf.models import Source
from bookshelf.source_citation import get_source_reference
from file_handling.models import PaperFile
from paper_work.models import Paper
from user_management.models import User
from .models import WorkSpace


def create_friendly_space_directory(work_space: WorkSpace) -> str | bool:
    """Creates user-friendly directory for future zip-archiving and downloading"""

    # Get all sources and papers in given work space
    sources = work_space.sources.all()
    papers = work_space.papers.filter(archived=False)

    if not sources and not papers:
        # In case work space is empty
        return False

    # Get all work space users
    owner, members = work_space.owner, work_space.members.all()
    if members:
        users = list(members)
        users.append(owner)
    else:
        users = [owner]

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

    # Return path to the whole dir
    return original_path


def create_friendly_sources_directory(work_space: WorkSpace) -> str | bool:
    """Creates user-friendly directory with all space-related sources for future zip-archiving"""

    # Get all sources in given work space
    sources = work_space.sources.all()
    if not sources:
        return False

    # Create new empty directory
    work_space.create_friendly_dir()
    original_path = work_space.get_friendly_path()
    root_path = os.path.join(original_path, "Sources")

    # Create new "sources" dir
    create_friendly_sources_dir(sources, root_path)

    # Return path to the whole dir
    return original_path


def create_friendly_sources_dir(sources, root_path: str) -> None:
    """Create new "books" dir with all space-related sources inside"""

    books_root = os.path.join(root_path, "sources")
    os.makedirs(books_root, exist_ok=True)

    # Get, quote and sort alphabetically all sources
    sources_apa = sorted([get_source_reference(source).endnote_apa for source in sources])
    sources_mla = sorted([get_source_reference(source).endnote_mla for source in sources])

    # Get paths to new .txt files
    apa_file_path = os.path.join(books_root, "sources_apa.txt")
    mla_file_path = os.path.join(books_root, "sources_mla.txt")

    # Create two new .txt files
    with open(apa_file_path, "w") as apa_file, open(mla_file_path, "w") as mla_file:
        source_counter = 1
        for i in range(len(sources)):
            # Write sources arrays into both files
            apa_file.write(f"{source_counter}. {sources_apa[i]}\n\n")
            mla_file.write(f"{source_counter}. {sources_mla[i]}\n\n")
            source_counter += 1

    # Get array with only sources which files were uploaded
    sources_with_files = [source for source in sources if source.has_file]

    if any(sources_with_files):
        # Create new "sources-files" dir
        sources_files_root = os.path.join(books_root, "files")
        os.makedirs(sources_files_root, exist_ok=True)

        for source in sources_with_files:
            # Copy original source file into new "sources-file" dir
            source: Source
            destination = os.path.join(sources_files_root, source.get_file().file_name())
            original_file = source.get_file().get_path_to_file()
            shutil.copyfile(original_file, destination)


def create_friendly_papers_dir(papers, authors: list, root_path: str) -> None:
    """Create new "papers" dir with all space-related papers inside"""

    papers_root = os.path.join(root_path, "papers")
    os.makedirs(papers_root, exist_ok=True)

    # Get all users
    for author in authors:
        # Get all user papers
        author_papers = [paper for paper in papers if paper.user == author]

        # Add only whose users who creates a paper
        if any(author_papers):
            author: User
            if len(authors) == 1:
                # Don't create author dir if there is only one user
                author_root = papers_root
            else:
                # Create new "user" dirs inside "papers" dir if there are multiple users
                author_name = f"{author.last_name} {author.first_name}"
                author_root = os.path.join(papers_root, author_name)
                os.makedirs(author_root, exist_ok=True)

            for author_paper in author_papers:
                # Create new "paper" dirs inside "user" dir
                author_paper: Paper
                path_to_paper = os.path.join(author_root, author_paper.title)
                os.makedirs(path_to_paper, exist_ok=True)

                # Get all paper-related files
                files = author_paper.files.all()
                for file in files:
                    # Create new "paper-file" dirs inside "paper" dir
                    file: PaperFile
                    path_to_paper_file = os.path.join(path_to_paper, str(file))
                    os.makedirs(path_to_paper_file, exist_ok=True)

                    # Copy original paper file into new "paper-file" dir
                    destination = os.path.join(path_to_paper_file, file.file_name())
                    original_file = file.get_path_to_file()
                    shutil.copyfile(original_file, destination)
