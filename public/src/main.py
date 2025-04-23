import os
import shutil

def copy_static(source_dir, dest_dir):
    """
    Recursively copy files from source_dir to dest_dir.
    First deletes dest_dir if it exists, then recreates it.
    """
    # Check if destination exists, if so, delete it first
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    os.mkdir(dest_dir)
    
    # Get all items in the source directory
    items = os.listdir(source_dir)
    
    # Loop through each item
    for item in items:
        # Create full paths
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        
        # Check if it's a file or directory
        if os.path.isfile(source_item):
            # Copy the file
            shutil.copy(source_item, dest_item)
            print(f"Copied file: {source_item} to {dest_item}")
        else:
            # It's a directory - create it in destination
            os.mkdir(dest_item)
            print(f"Created directory: {dest_item}")
            
            # Recursively copy contents of this subdirectory
            copy_static(source_item, dest_item)

def main():
    """
    Main function that initiates the static file copying process
    from the 'static' directory to the 'public' directory.
    """
    #copy_static("static", "public")

if __name__ == "__main__":
    # Only execute when script is run directly, not when imported
    main()