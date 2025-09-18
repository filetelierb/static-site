from file_management import copy_dir, generate_pages_recursive
def main():
    copy_dir()
    generate_pages_recursive('./content', './template.html', './public')
   
main()