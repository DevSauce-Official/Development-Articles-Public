import json
import os
import shutil

def main():
    # 1. Get Input From Workflow (unchanged) 
    json_file_path = os.environ.get("INPUT_JSON_FILE_PATH")

    if not json_file_path:
        print("::error:: Missing 'json_file_path' input")
        exit(1)

    # 2. Read and Parse JSON File (unchanged) 
    try:
        with open(json_file_path, "r") as f:
            instructions = json.load(f)
    except FileNotFoundError:
        print(f"::error:: File not found: {json_file_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"::error:: Invalid JSON in file: {json_file_path}")
        exit(1)

    # 3. Execute Instructions
    action_type = instructions.get("action_type")
    message = instructions.get("message", "Automated Repository Update")

    if action_type == "create_file":
        create_file(instructions)
    elif action_type == "update_file":
        update_file(instructions)
    elif action_type == "create_folder":
        create_folder(instructions)
    elif action_type == "delete_file":
        delete_file(instructions)
    elif action_type == "delete_folder":
        delete_folder(instructions)
    else:
        print(f"::error:: Invalid action type: {action_type}")
        exit(1)

    print(f"::set-output name=commit_message::{message}")

# ---- Action Functions (Fully Implemented) ----

def create_file(instructions):
    """Creates a new file."""
    file_path = instructions.get("file_path")
    content = instructions.get("file_content")
    overwrite = instructions.get("overwrite", False)

    if not file_path or not content:
        print("::error:: 'file_path' and 'file_content' are required for 'create_file'.")
        exit(1)

    if os.path.exists(file_path) and not overwrite:
        print(f"::warning:: File already exists: {file_path}. Skipping...")
        return

    try:
        with open(file_path, "w", encoding='utf-8') as f: 
            f.write(content) 
        print(f"::debug:: Created file: {file_path}")
    except Exception as e:
        print(f"::error:: Failed to create file {file_path}: {e}")
        exit(1)

def update_file(instructions):
    """Updates an existing file."""
    file_path = instructions.get("file_path")
    update_mode = instructions.get("update_mode")
    content = instructions.get("content")
    line_number = instructions.get("line_number")

    if not file_path or not update_mode or not content:
        print("::error:: 'file_path', 'update_mode', and 'content' are required for 'update_file'.")
        exit(1)

    if not os.path.exists(file_path):
        print(f"::error:: File not found: {file_path}")
        exit(1)

    try:
        with open(file_path, "r+", encoding='utf-8') as f:
            file_content = f.readlines()
            if update_mode == "replace":
                f.seek(0)
                f.write(content)
                f.truncate()
            elif update_mode == "append":
                f.seek(0, 2)  # Seek to end of file
                f.write(content)
            elif update_mode == "prepend":
                f.seek(0) 
                f.write(content + "".join(file_content)) 
            elif update_mode == "insert_after_line":
                if line_number is None:
                    print("::error:: 'line_number' is required for 'insert_after_line' mode.")
                    exit(1)
                if line_number > len(file_content) or line_number <= 0:
                    print(f"::error:: Invalid line number: {line_number}")
                    exit(1) 
                file_content.insert(line_number, content + "\n") # Insert content after the given line
                f.seek(0) 
                f.write("".join(file_content))
                f.truncate() 
            else:
                print(f"::error:: Invalid update mode: {update_mode}")
                exit(1) 

        print(f"::debug:: Updated file: {file_path} (Mode: {update_mode})") 

    except Exception as e:
        print(f"::error:: Failed to update file {file_path}: {e}")
        exit(1)

def create_folder(instructions):
    """Creates a new folder."""
    folder_path = instructions.get("folder_path") 

    if not folder_path:
        print("::error:: 'folder_path' is required for 'create_folder'.")
        exit(1)

    if os.path.exists(folder_path):
        print(f"::warning:: Folder already exists: {folder_path}. Skipping...")
        return

    try:
        os.makedirs(folder_path) 
        print(f"::debug:: Created folder: {folder_path}") 
    except Exception as e:
        print(f"::error:: Failed to create folder {folder_path}: {e}")
        exit(1)

def delete_file(instructions): 
    """Deletes a file.""" 
    file_path = instructions.get("file_path")
    if not file_path: 
        print("::error:: 'file_path' is required for 'delete_file'.")
        exit(1)
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path) 
            print(f"::debug:: Deleted file: {file_path}")
        except Exception as e: 
            print(f"::error:: Failed to delete file {file_path}: {e}")
            exit(1)
    else: 
        print(f"::warning:: File does not exist: {file_path}")
        
def delete_folder(instructions):
    """Deletes a folder."""
    folder_path = instructions.get("folder_path")
    if not folder_path:
        print("::error:: 'folder_path' is required for 'delete_folder'.")
        exit(1)

    if os.path.exists(folder_path):
        try: 
            shutil.rmtree(folder_path)
            print(f"::debug:: Deleted folder: {folder_path}") 
        except  Exception  as  e:
           print(f"::error::  Failed to delete folder {folder_path}:  {e}") 
            exit(1) 
    else:
        print(f"::warning:: Folder does not exist:  {folder_path}")


if __name__ == "__main__":
    main()
