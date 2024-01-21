import os
import shutil
from bookshelf.source_copying import copy_source
from user_management.models import User
from work_space.models import WorkSpace


def create_new_space(owner: User, title: str) -> int:
    """Creates new Workspace obj"""
    new_space = WorkSpace(owner=owner, title=title)
    new_space.save()
    new_space.create_dir()
    return new_space.pk


def copy_space_with_all_sources(original_space: WorkSpace, new_owner: User) -> WorkSpace:
    """Copy work space and all its sources into the new work space"""

    # Get all original sources
    original_sources = original_space.sources.all()
    if not original_sources:
        return False
    
    # Create new Workspace obj
    new_space_title = f"{original_space.title} by {original_space.owner}"
    new_space = create_new_space(new_owner, new_space_title)

    # Copy all sources into db and keep track of new sources id
    new_sources_id: dict = {}
    for source in original_sources:
      new_source = copy_source(source, new_space, new_owner)
      new_sources_id[source.pk] = new_source.pk

    # Get array with only sources which files were uploaded
    sources_with_files = [source for source in original_sources if source.file]

    # Copy all files if necessary
    if any(sources_with_files):
        # Create new "sources" dir
        new_sources_root = os.path.join(new_space.get_path(), "sources", f"user_{new_owner.pk}")
        os.makedirs(new_sources_root, exist_ok=True)

        for source in sources_with_files:
            # Copy original source file into new "sources-files" dir
            new_source_id = new_sources_id[source.pk]
            source_id_root = os.path.join(new_sources_root, f"source_{new_source_id}")
            os.makedirs(source_id_root, exist_ok=True)
            destination = os.path.join(source_id_root, source.file.file_name())
            original_file = source.get_path_to_file()
            shutil.copyfile(original_file, destination)

    # Return new Workspace obj       
    return new_space
