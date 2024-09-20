import os
import pywikibot
from pywikibot import pagegenerators

# Configuration for pywikibot
pywikibot.config.family = 'commons'
pywikibot.config.mylang = 'commons'

# Connect to Wikimedia Commons
site = pywikibot.Site()

# Replace 'Category:Example' with your desired category
category_name = 'Category:19th-century_engravings'  # Enter your category name here
cat = pywikibot.Category(site, category_name)

# This will iterate through all images in the category
gen = pagegenerators.CategorizedPageGenerator(cat)

# Directory where files will be downloaded
download_directory = '/mnt/c/Users/beckett.mcfarland/Pictures/Wikimedia/'  # Update this path

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

for page in gen:
    if page.namespace() == 6:  # Checking if it's a File namespace
        # Get the file page
        file_page = pywikibot.FilePage(page)
        
        # Get the file URL
        file_url = file_page.get_file_url()
        
        # Get the file name
        file_name = os.path.join(download_directory, file_page.title(with_ns=False))
        
        # Download the file
        file_page.download(file_name)
        print(f'Downloaded: {file_name}')

