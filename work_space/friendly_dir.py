import os
import shutil

from bookshelf.quoting_apa import quote_source_apa
from bookshelf.quoting_mla import quote_source_mla
from work_space.models import WorkSpace


# Much to be done!

def create_friendly_dir(work_space: WorkSpace) -> str:
    """Creates user-friendly directory for future zip-archiving and downloading"""

    # Get all books and papers in given work space
    papers, sources = work_space.papers.all(), work_space.sources.all()

    if not papers and not sources:
        # In case work space is empty
        return False
        
    # Create new empty directory
    work_space.create_friendly_dir()
    original_path = work_space.get_friendly_path()
    root_path = os.path.join(original_path, work_space.title)

    if papers:
        # Create new "papers" dir
        papers_root = os.path.join(root_path, "papers")
        os.makedirs(papers_root, exist_ok=True)

        # Get all users
        authors = [paper.user for paper in papers]

        for author in authors:
            if len(set(authors)) != 1:
                # Create new "user" dirs inside "papers" dir if there are multiple users
                author_name = f"{author.last_name} {author.first_name}"
                author_root = os.path.join(papers_root, author_name)
                os.makedirs(author_root, exist_ok=True)
            else:
                # Don't create author dir if there is only one user
                author_root = papers_root

            # Get all user papers
            author_papers = papers.filter(user=author)

            for author_paper in author_papers:
                # Create new "paper" dirs inside "user" dir
                path_to_paper = os.path.join(author_root, author_paper.title)
                os.makedirs(path_to_paper, exist_ok=True)

                # Get all paper-related files
                versions = author_paper.versions.all()
                for version in versions:
                    # Create new "paper-file" dirs inside "paper" dir
                    path_to_paper_version = os.path.join(path_to_paper, version.get_saving_time())
                    os.makedirs(path_to_paper_version, exist_ok=True)

                    # Copy original paper file into new "paper-file" dir
                    destination = os.path.join(path_to_paper_version, version.file_name())
                    original_file = version.get_full_path()
                    shutil.copyfile(original_file, destination)
                    
    if sources:
        # Sources!!!!
        # Variables!!!!

        # Create new "books" dir
        books_root = os.path.join(root_path, "books")
        os.makedirs(books_root, exist_ok=True)

        # Get, quote and sort alphabetically all books
        sources_apa = sorted([quote_source_apa(source) for source in sources])
        sources_mla = sorted([quote_source_mla(source) for source in sources])

        # Get paths to new .txt files
        apa_file_path = os.path.join(books_root, "books_apa.txt")
        mla_file_path = os.path.join(books_root, "books_mla.txt")

        # Create two new .txt files
        with open(apa_file_path, "w") as apa_file, open(mla_file_path, "w") as mla_file:

            book_counter = 1
            for i in range(len(sources)):
                # Write sources arrays into both files
                apa_file.write(f"{book_counter}. {sources_apa[i]}\n")
                mla_file.write(f"{book_counter}. {sources_mla[i]}\n")
                book_counter += 1

        # Get array with only books which files were uploaded
        sources_with_files = [source for source in sources if source.file]

        if any(sources_with_files):
            # Create new "books-files" dir
            book_files_root = os.path.join(books_root, "files")
            os.makedirs(book_files_root, exist_ok=True)

            for source in sources_with_files:
                # Copy original book file into new "books-file" dir
                destination = os.path.join(book_files_root, source.file_name())
                original_file = source.get_path_to_file()
                shutil.copyfile(original_file, destination)

        # Get array with only books with quotes
        sources_with_quotes = [source for source in sources if source.quotes.all()]

        if any(sources_with_quotes):
            
            # Get paths to new .txt file
            quotes_file = os.path.join(books_root, "quotes.txt")

            # Create file and write in all quotes
            with open(quotes_file, "w") as file:

                for source in sources_with_quotes:
                    # Write every book title
                    file.write(f"\t{source}\n\n\n")
                    book_quotes = source.quotes.all()
                    # Write all its quotes
                    for quote in book_quotes:
                        file.write(f"{quote}\n\n")
                    file.write("\n\n")

    # Return path to the whole dir
    return original_path
