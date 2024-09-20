import subprocess

def run_powershell_command(command):
    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")

def add_members_to_group(group_name, sam_account_names):
    members = ','.join([f'"{sam}"' for sam in sam_account_names])
    command = f"Import-Module ActiveDirectory; Add-ADGroupMember -Identity '{group_name}' -Members {members}"
    run_powershell_command(command)

def remove_members_from_group(group_name, sam_account_names):
    members = ','.join([f'"{sam}"' for sam in sam_account_names])
    command = f"Import-Module ActiveDirectory; Remove-ADGroupMember -Identity '{group_name}' -Members {members} -Confirm:$false"
    run_powershell_command(command)

if __name__ == "__main__":
    group_email = input("Enter the email of the distribution group: ")
    group_name = f"CN={group_email},CN=Users,DC=example,DC=com"  # Adjust this format based on your AD structure
    
    action = input("Do you want to add or remove members? (add/remove): ").strip().lower()
    
    sam_names_input = input("Enter the SAM account names separated by commas: ")
    sam_account_names = [name.strip() for name in sam_names_input.split(",")]
    
    if action == "add":
        add_members_to_group(group_name, sam_account_names)
    elif action == "remove":
        remove_members_from_group(group_name, sam_account_names)
    else:
        print("Invalid action. Please enter 'add' or 'remove'.")
