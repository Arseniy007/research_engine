import shutil
import os


def create_friendly_dir(work_space):

    papers = work_space.papers.all()
    books = work_space.books.all()

    if not papers and not books:
        #return JsonResponse({"message": "Empty Work Space"})
        pass

    work_space.create_friendly_dir()

    root_path = work_space.get_friendly_path()

    if papers:

        papers_root = f"{root_path}/papers"

        os.mkdir(papers_root)

        authors = [paper.user for paper in papers]

        for author in authors:

            author_name = f"{author.last_name} {author.first_name}"

            author_root = os.path.join(papers_root, author_name)
            os.makedirs(author_root, exist_ok=True)

            author_papers = papers.filter(user=author)

            for author_paper in author_papers:

                path_to_paper = os.path.join(author_root, author_paper)
                os.makedirs(path_to_paper, exist_ok=True)

                versions = author_paper.versions.all()

                for version in versions:

                    path_to_paper_version = os.path.join(path_to_paper, version.get_saving_time())
                    os.makedirs(path_to_paper_version, exist_ok=True)

                    file_name = version.file_name()

                    original_file = version.get_full_path()
                    destination = os.path.join(path_to_paper_version, file_name)

                    shutil.copyfile(original_file, destination)
    
    if books:

        # TODO
        # Create a txt/exel etc. file for all books (not book files)?
        pass