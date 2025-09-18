from file_management import copy_dir, generate_pages_recursive
import sys

def main():
    copy_dir()
    
    basepath = sys.argv[0] if len(sys.argv) > 0 else '/'
    generate_pages_recursive('./content', './template.html', './docs', basepath)
   
main()