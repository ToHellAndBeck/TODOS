import subprocess
import json


def update_ad_user(sam_account_names, field, new_value):
    for sam_account_name in sam_account_names:
        command = [
            "powershell",
            "-Command",
            "Import-Module ActiveDirectory; Set-ADUser -Identity '{sam_account_name}' -{field} '{new_value}'".format(
                sam_account_name=sam_account_name, field=field, new_value=new_value)
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully updated {field} for user {sam_account_name} to {new_value}.")
        else:
            print(f"Error: PowerShell command failed with return code {result.returncode} for user {sam_account_name}.")
            print("PowerShell stderr:", result.stderr)


def add_user_to_group(sam_account_names, group_names):
    for group_name in group_names:
        command = [
            "powershell",
            "-Command",
            "Import-Module ActiveDirectory; Add-ADGroupMember -Identity '{group_name}' -Members {members}".format(
                group_name=group_name, members=','.join(["'{}'".format(sam) for sam in sam_account_names]))
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully added users {', '.join(sam_account_names)} to group {group_name}.")
        else:
            print(f"Error: PowerShell command failed with return code {result.returncode} for group {group_name}.")
            print("PowerShell stderr:", result.stderr)


def remove_user_from_group(sam_account_names, group_names):
    for group_name in group_names:
        command = [
            "powershell",
            "-Command",
            "Import-Module ActiveDirectory; Remove-ADGroupMember -Identity '{group_name}' -Members {members} -Confirm:$false".format(
                group_name=group_name, members=','.join(["'{}'".format(sam) for sam in sam_account_names]))
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully removed users {', '.join(sam_account_names)} from group {group_name}.")
        else:
            print(f"Error: PowerShell command failed with return code {result.returncode} for group {group_name}.")
            print("PowerShell stderr:", result.stderr)


def change_user_passwords(sam_account_names, new_password):
    import_module_command = """
    try {
        [System.Management.Automation.PSTypeRegistry]::GetCustomTypes().Remove('System.Security.AccessControl.ObjectSecurity')
        Import-Module Microsoft.PowerShell.Security -ErrorAction Stop
    } catch {
        Write-Host "Failed to load module Microsoft.PowerShell.Security: $_" -ForegroundColor Red
    }
    """

    # Load the module once
    result = subprocess.run(["powershell", "-Command", import_module_command], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: Failed to load Microsoft.PowerShell.Security module.")
        print("PowerShell stderr:", result.stderr)
        return

    # Change passwords for each user
    for sam_account_name in sam_account_names:
        command = """
        $pass = ConvertTo-SecureString '{new_password}' -AsPlainText -Force
        Set-ADAccountPassword -Identity '{sam_account_name}' -Reset -NewPassword $pass
        """.format(sam_account_name=sam_account_name, new_password=new_password)

        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully changed password for user {sam_account_name}.")
        else:
            print(f"Error: PowerShell command failed with return code {result.returncode} for user {sam_account_name}.")
            print("PowerShell stderr:", result.stderr)


def search_ad(query, fields, searchby, object_type):
    if object_type not in ['user', 'group']:
        print("Invalid object type. Please enter 'user' or 'group'.")
        return None

    filter_query = f"{searchby} -like '*{query}*'"
    properties = ','.join(fields)
    select_properties = ','.join(fields)

    command = [
        "powershell",
        "-Command",
        f"Import-Module ActiveDirectory; Get-AD{object_type.capitalize()} -Filter \"{filter_query}\" -Properties {properties} | Select-Object {select_properties} | ConvertTo-Json -Compress"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        if result.stdout:
            try:
                # Ensure the output starts with a JSON object or array
                json_start = result.stdout.find('[')
                if json_start == -1:
                    json_start = result.stdout.find('{')
                if json_start != -1:
                    json_data = result.stdout[json_start:]
                    parsed_output = json.loads(json_data)
                    if isinstance(parsed_output, dict):
                        return [parsed_output]
                    return parsed_output
                else:
                    print("Error: No JSON found in the PowerShell output.")
                    return None
            except json.JSONDecodeError as e:
                print("Error: Failed to decode JSON. The output may be improperly formatted.")
                print("JSONDecodeError:", e)
                return None
        else:
            print("Error: No output received from PowerShell command.")
            return None
    else:
        print(f"Error: PowerShell command failed with return code {result.returncode}.")
        print("PowerShell stderr:", result.stderr)
        return None


def main():
    actions = {
        "1": "search",
        "2": "update",
        "3": "addgroup",
        "4": "removegroup",
        "5": "changepassword"
    }

    action = input("Enter the number corresponding to your action:\n1. Search\n2. Update\n3. Add to group\n4. Remove from group\n5. Change passwords\n").strip()

    if action not in actions:
        print("Invalid action. Please enter a number between 1 and 5.")
        return

    action = actions[action]

    if action == 'search':
        object_type = input("Enter the object type you want to search for ('user' or 'group'): ").strip().lower()
        searchby = input("Enter the field you want to search by (Name, SamAccountName, DistinguishedName, Description, Manager, etc.): ")
        query = input("Enter your search query (comma-separated if multiple): ").strip()
        queries = [q.strip() for q in query.split(",")]
        fields = input("Enter the fields you want to retrieve (comma-separated): ").strip()
        fields_list = [field.strip() for field in fields.split(",")]

        for q in queries:
            result = search_ad(q, fields_list, searchby, object_type)
            print("-" * 20)
            if result:
                for item in result:
                    for field in fields_list:
                        print(f"{field}: {item.get(field, 'N/A')}")
                    print("-" * 20)
            else:
                print("No results found or an error occurred.")
    elif action == 'update':
        sam_account_names = input("Enter the SAM account names of the users you want to update (comma-separated): ").strip()
        sam_account_name_list = [sam.strip() for sam in sam_account_names.split(",")]
        field = input("Enter the field you want to update (e.g., DisplayName, Title, Department): ").strip()
        new_value = input(f"Enter the new value for {field}: ").strip()
        update_ad_user(sam_account_name_list, field, new_value)
    elif action == 'addgroup':
        sam_account_names = input("Enter the SAM account names of the users you want to add to a group (comma-separated): ").strip()
        group_names = input("Enter the names of the groups (comma-separated): ").strip()
        sam_account_name_list = [sam.strip() for sam in sam_account_names.split(",")]
        group_name_list = [group.strip() for group in group_names.split(",")]
        add_user_to_group(sam_account_name_list, group_name_list)
    elif action == 'removegroup':
        sam_account_names = input("Enter the SAM account names of the users you want to remove from a group (comma-separated): ").strip()
        group_names = input("Enter the names of the groups (comma-separated): ").strip()
        sam_account_name_list = [sam.strip() for sam in sam_account_names.split(",")]
        group_name_list = [group.strip() for group in group_names.split(",")]
        remove_user_from_group(sam_account_name_list, group_name_list)
    elif action == 'changepassword':
        sam_account_names = input("Enter the SAM account names of the users you want to change passwords for (comma-separated): ").strip()
        new_password = input("Enter the new password: ").strip()
        sam_account_name_list = [sam.strip() for sam in sam_account_names.split(",")]
        change_user_passwords(sam_account_name_list, new_password)


if __name__ == "__main__":
    main()
