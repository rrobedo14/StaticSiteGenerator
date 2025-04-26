import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"  # Change this line   #"./public"
dir_path_content = "./content"
template_path = "./template.html"
basepath = "/" if len(sys.argv) < 2 else sys.argv[1]

def main():
    print("Deleting public directory..")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages recursively...")
    generate_pages_recursive(
        dir_path_content,  # The content directory to crawl
        template_path,     # The template to use
        dir_path_public,   # The destination directory
        basepath           #
    )

main()

