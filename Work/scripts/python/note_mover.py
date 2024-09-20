import os
import shutil

def move_notes_to_root(root_dir):
    # Iterate over all files and subdirectories in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip the root directory itself
        if dirpath == root_dir:
            continue
        
        for filename in filenames:
            if filename.endswith(".md"):
                # Construct the full file path
                file_path = os.path.join(dirpath, filename)
                # Construct the new file path in the root directory
                new_file_path = os.path.join(root_dir, filename)
                
                # Move the file to the root directory
                shutil.move(file_path, new_file_path)
        
        # Remove the subdirectory if it is empty
        if not os.listdir(dirpath):
            os.rmdir(dirpath)

# Replace '/path/to/notes' with the actual path to your notes directory
notes_directory = '/mnt/c/Users/beckett.mcfarland/Documents/Obsidian/The Beck Vault/'
move_notes_to_root(notes_directory)

