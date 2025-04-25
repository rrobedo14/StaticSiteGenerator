import os
from block_markdown_converter import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()

    for line in lines:
        if line.startswith("# "):
            # Remove the "# " prefix and strip any remaining whitespace
            return line[2:].strip()
    
    # If we get here, we've checked all lines and found no header
    raise Exception("No header found")


def generate_page(from_path, template_path, dest_path, basepath):
    # 1. Print a message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # 2. Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # 3. Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # 4. Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # 5. Extract the title
    title = extract_title(markdown_content)
    
    # 6. Replace placeholders in the template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    # 7. Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # 8. Write the final HTML to the destination
    with open(dest_path, 'w') as f:
        f.write(final_html)
        

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Check if the content directory exists
    if not os.path.exists(dir_path_content):
        print(f"Warning: Content directory {dir_path_content} does not exist")
        return
    
    # List all entries in the content directory
    entries = os.listdir(dir_path_content)
    
    # Process each entry
    for entry in entries:
        # Create full path for the current entry
        entry_path = os.path.join(dir_path_content, entry)
        
        # Check if it's a file or directory
        if os.path.isfile(entry_path):
            # Only process markdown files
            if entry_path.endswith('.md'):
                # Calculate relative path from content root
                rel_path = os.path.relpath(entry_path, dir_path_content)
                
                # Create destination path with .html extension
                dest_path = os.path.join(dest_dir_path, 
                                        os.path.splitext(rel_path)[0] + '.html')
                
                # Generate the page
                print(f"Processing {rel_path} -> {os.path.relpath(dest_path, dest_dir_path)}")
                generate_page(entry_path, template_path, dest_path, basepath)
        elif os.path.isdir(entry_path):
            # It's a directory, recursively process it
            new_content_dir = entry_path
            new_dest_dir = os.path.join(dest_dir_path, entry)
            # Ensure the destination directory exists
            os.makedirs(new_dest_dir, exist_ok=True)
            # Recursively process the subdirectory
            generate_pages_recursive(new_content_dir, template_path, new_dest_dir, basepath)