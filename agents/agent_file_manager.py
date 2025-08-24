import re
import os
import zipfile

def extract_files_from_transcript(messages):
    """
    Extracts code/file blocks from a list of chat messages.
    """
    pattern = r'---([\w./-]+)---\s*([\s\S]+?)(?=(---[\w./-]+---|$))'
    files = {}
    for msg in messages:
        if hasattr(msg, "content"):
            for match in re.finditer(pattern, msg.content):
                filename = match.group(1).strip()
                code = match.group(2).strip()
                files[filename] = code
    return files

def save_files_to_project(files_dict, project_root):
    if not os.path.exists(project_root):
        os.makedirs(project_root)
    for file_path, content in files_dict.items():
        full_path = os.path.join(project_root, file_path)
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)


def zip_project_directory(project_dir, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                abs_file_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_file_path, project_dir)
                zipf.write(abs_file_path, rel_path)