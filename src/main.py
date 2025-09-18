from file_management import copy_dir, generate_pages_recursive
import sys

def main():
    copy_dir()
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    print(f"Basepath set to: {basepath}")
    generate_pages_recursive('./content', './template.html', './docs', basepath)
   
main()