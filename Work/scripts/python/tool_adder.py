import openpyxl
from openpyxl.styles import Font

def get_input(prompt, allow_empty=False):
    while True:
        value = input(prompt)  # Preserves leading/trailing spaces
        if value or allow_empty:
            return value
        print("This field cannot be empty. Please try again.")

def create_asset_inventory():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Asset Inventory"

    # Define all headers
    all_headers = [
        "DEPARTMENT", "ASSET TAG", "SCAN CODE", "TOOL STATUS", "TOOL TYPE", "MODEL",
        "MANUFACTURER", "SERIAL NUMBER", "VENDOR", "PURCHASE DATE", "PURCHASE PRICE",
        "RETIRED DATE", "WARRANTY EXPIRATION", "NEXT CALIBRATION DATE", "ASSIGNED TO JOB NUMBER",
        "ASSIGNED TO WJID", "ASSIGNED TO WAREHOUSE", "WAREHOUSE AREA", "ASSIGNED TO PERSON",
        "NOTES", "REQUIRE ADMIN APPROVAL ON TRANSFER"
    ]

    # Add all headers to the worksheet
    for col, header in enumerate(all_headers, start=1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)

    # Define headers to prompt for (excluding VENDOR)
    prompt_headers = [
        "DEPARTMENT", "ASSET TAG", "SCAN CODE", "TOOL STATUS", "TOOL TYPE", "MODEL",
        "MANUFACTURER", "SERIAL NUMBER", "PURCHASE DATE", "PURCHASE PRICE",
        "RETIRED DATE", "WARRANTY EXPIRATION", "NEXT CALIBRATION DATE", "ASSIGNED TO JOB NUMBER",
        "ASSIGNED TO WJID", "ASSIGNED TO WAREHOUSE", "WAREHOUSE AREA", "ASSIGNED TO PERSON",
        "NOTES", "REQUIRE ADMIN APPROVAL ON TRANSFER"
    ]

    # Get user input for specified fields
    row_data = []
    for header in all_headers:
        if header in prompt_headers:
            if header in ["PURCHASE PRICE", "RETIRED DATE", "WARRANTY EXPIRATION", "NEXT CALIBRATION DATE", "NOTES"]:
                value = get_input(f"Enter {header} (press Enter to skip): ", allow_empty=True)
            elif header == "TOOL STATUS":
                value = get_input(f"Enter {header} (Active/Inactive): ")
            elif header == "REQUIRE ADMIN APPROVAL ON TRANSFER":
                value = get_input(f"{header}? (Yes/No): ")
            else:
                value = get_input(f"Enter {header}: ")
        else:
            value = ""  # Leave blank for headers not in prompt_headers
        row_data.append(value)

    # Add the data to the worksheet
    ws.append(row_data)

    # Save the workbook
    filename = r"C:\Users\beckett.mcfarland\Documents\Tool Import\ToolImportTemplate2.xlsx"
    wb.save(filename)
    print(f"Asset inventory has been saved to {filename}")

if __name__ == "__main__":
    create_asset_inventory()
