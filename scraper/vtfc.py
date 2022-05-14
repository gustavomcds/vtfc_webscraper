import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_most_used_verbs(url) -> dict:

    """
    Get most used verbs from the VTFC's homepage

    ### Parameters
    1. url : str
        - VTFC's homepage url
    """

    page = requests.get(url)

    html = BeautifulSoup(page.text, 'html.parser')

    list_verbs = html.find('div', class_='verb-list').find('div', class_='text').find_all('a', class_='verb')

    dict_verbs = dict()

    for verb in list_verbs:
        dict_verbs[verb.text] = 'https://www.gymglish.com' + verb['href']

    return dict_verbs

def get_one_verb_conjugation(url, strip_conjug_verb) -> dict:

    """
    Get most used verbs from the VTFC's homepage

    ### Parameters
    1. url : str
        - VTFC's verb page url
    2. strip_conjug_verb : boolean
        - If true, applies str.strip() method to the conjugated verb string
    """
    
    page = requests.get(url)

    html = BeautifulSoup(page.text, 'html.parser')

    all_tenses = html.find('main', class_='container').find('div', class_='row').find_all('div')

    dict_verb_conjugations = dict()

    for tense in all_tenses:    

        dict_verb_conjugations[tense.find('h3', class_='tense-name').text] = list()

        conjugations = tense.find('ul', class_='conjucation-forms').find_all('li')

        for conjugation in conjugations:

            try:

                dict_verb_conjugations[tense.find('h3', class_='tense-name').text].append(
                    {
                        'pronoun' : conjugation.find(text=True).lstrip(), 
                        'conjugated_verb' : conjugation.find('span').text.strip() if strip_conjug_verb else conjugation.find('span').text
                    }
                )

            except Exception as e:

                pass

    return dict_verb_conjugations

def get_most_used_verbs_conjugations(url_most_used_verbs, strip_conjug_verb) -> dict:

    """
    Get most used verbs from the VTFC's homepage

    ### Parameters
    1. url : str
        - VTFC's homepage url
    2. strip_conjug_verb : boolean
        - If true, applies str.strip() method to the conjugated verb string
    """

    dict_most_used_verbs = get_most_used_verbs(url_most_used_verbs)

    keys = list(dict_most_used_verbs.keys())

    dict_most_used_verbs_conjugations = dict()

    for key in tqdm(keys):

        try:

            dict_most_used_verbs_conjugations[key] = get_one_verb_conjugation(dict_most_used_verbs[key], strip_conjug_verb)

        except Exception as e:

            pass

    return dict_most_used_verbs_conjugations