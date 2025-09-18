import os
import shutil
from md_to_html import markdown_to_html_node, extract_title

def copy_dir(src_dir='./static', dest_dir='./docs'):
    """
    Clears all contents of the specified public directory.

    Args:
        public_dir (str): The path to the public directory to be cleared.
    """
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    entries = os.listdir(src_dir)
    for entry in entries:
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)
        if os.path.isdir(src_path):
            copy_dir(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    from_file = open(from_path, 'r')
    content = from_file.read()

    template_file = open(template_path, 'r')
    template = template_file.read()

    node = markdown_to_html_node(content)
    html_content = node.to_html()
    title = extract_title(content)

    final_html = template.replace("{{ Content }}", html_content).replace("{{ Title }}", title)
    final_html = final_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    dest_file = open(dest_path, 'w')
    dest_file.write(final_html)
    dest_file.close()
    from_file.close()
    template_file.close()
    print(f"Page generated at {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    entries = os.listdir(dir_path_content)
    for entry in entries:
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
        elif entry.endswith('.md'):
            dest_file_path = dest_path[:-3] + '.html'  # Change .md to .html
            generate_page(src_path, template_path, dest_file_path, basepath)

