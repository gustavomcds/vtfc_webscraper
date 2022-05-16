# Importing libs
import os
import yaml
import scraper.vtfc as VTFC
from scraper.export import export_to_csv, export_to_json, export_to_sqlite

# Reading parameters file
with open(os.path.join('config', 'params.yaml'), 'r') as file:
    params = yaml.safe_load(file)

# Choose between FR and ENG
LANG = input('Choose the language (FR or ENG): ')

if LANG == 'FR':
    print('You chose french')
elif LANG == 'ENG':
    print('You chose english')
else:
    print('Invalid option, choose between FR and ENG')

# Setting parameters based on user's choice
OUTPUTFILENAME = params['OUTPUTFILENAME_FR'] if LANG == 'FR' else params['OUTPUTFILENAME_ENG']
HOME_URL = params['HOME_URL_FR'] if LANG == 'FR' else params['HOME_URL_ENG']
STRIP_CONJUG_VERB = False if LANG == 'FR' else True

# Scraping data
dict_most_used_verbs_conjugations = VTFC.get_most_used_verbs_conjugations(HOME_URL, strip_conjug_verb=STRIP_CONJUG_VERB)

# Setting output filepath
output_filepath = os.path.join(params['OUTPUTFOLDERNAME'], OUTPUTFILENAME)

# Exporting data to json and csv files
export_to_json(dict_most_used_verbs_conjugations, f"{output_filepath}.json")
export_to_csv(dict_most_used_verbs_conjugations, f"{output_filepath}.csv")

# Exporting to SQLite database
export_to_sqlite(dict_most_used_verbs_conjugations, os.getcwd())