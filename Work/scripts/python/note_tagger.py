import os

def add_tags_to_notes(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Extract the folder name and replace spaces with underscores
        tag = os.path.basename(dirpath).replace(' ', '_')
        
        for filename in filenames:
            if filename.endswith(".md"):  # Only process .md files
                file_path = os.path.join(dirpath, filename)
                
                with open(file_path, 'r') as file:
                    content = file.readlines()
                
                # Check if the first line is a tag and replace it if necessary
                if content and content[0].startswith("#"):
                    content[0] = f"#{tag}\n"
                else:
                    content.insert(0, f"#{tag}\n")
                
                with open(file_path, 'w') as file:
                    file.writelines(content)# Replace '/path/to/notes' with the actual path to your notes directory

notes_directory = '/mnt/c/Users/beckett.mcfarland/Documents/Obsidian/The Beck Vault/'
add_tags_to_notes(notes_directory)

