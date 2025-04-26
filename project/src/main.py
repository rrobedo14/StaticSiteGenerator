import os
import shutil
import sys

from copystatic import copy_files_recursive
from generate_content import generate_pages_recursive


import os
import sys
import shutil

# Get the absolute path to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # src directory
project_dir = os.path.dirname(script_dir)  # project directory
repo_root = os.path.dirname(project_dir)  # repository root

# Set paths relative to the project directory for content and templates
dir_path_static = os.path.join(project_dir, "static")
dir_path_content = os.path.join(project_dir, "content")
template_path = os.path.join(project_dir, "template.html")

# Set docs path to repository root's docs directory
dir_path_public = os.path.join(repo_root, "docs")

basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
# dir_path_static = "./static"
# dir_path_public = "./docs"  # Change this line   #"./public"
# dir_path_content = "./content"
# template_path = "./template.html"
# basepath = "/" if len(sys.argv) < 2 else sys.argv[1]

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

