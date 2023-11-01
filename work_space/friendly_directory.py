import shutil
import os

from utils.verification import check_work_space

def delete_temporary_dir(function):
    """Decorator which deletes user-friendly dir after zip file has been sent"""
    def wrapper(request, space_id):

        # Call function
        function(request, space_id)

        # Get path to a temporary dir
        space = check_work_space(space_id, request.user)
        temporary_dir = space.get_friendly_path()

        if temporary_dir:
            # Delete it
            return shutil.rmtree(temporary_dir)
    return wrapper
            

def create_friendly_dir(work_space):
    """Creates user-friendly directory for future zip-archiving and downloading"""

    # Get all books and papers in given work space
    papers, books = work_space.papers.all(), work_space.books.all()

    if not papers and not books:
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

            author_name = f"{author.last_name} {author.first_name}"

            # Create new "user" dirs inside "papers" dir
            author_root = os.path.join(papers_root, author_name)
            os.makedirs(author_root, exist_ok=True)

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
    if books:
        # TODO
        # Create a txt/exel etc. file for all books (not book files)?
        pass
    
    # Return path to the whole dir
    return original_path
