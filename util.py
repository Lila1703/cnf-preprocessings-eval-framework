import os.path as path
from os import makedirs

def get_comments_string(input_path):
    with open(input_path, 'r') as file:
        comments = []
        for line in file:
            if line.startswith("c"):
                comments.append(line)
            else:
                break
    return ''.join(comments)


def preprend_content(part_to_prepent, input_path):
    with open(input_path, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(part_to_prepent + original_content)


def get_temp_dimacs_path(original_dimacs, preprocessor_name, keep_dimacs = False):
    if not keep_dimacs:
        return 'temp.dimacs'
    makedirs('preprocessed_dimacs', exist_ok=True)
    return path.join('preprocessed_dimacs', f'{preprocessor_name}-{path.basename(original_dimacs)}')
    
