import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))
from scraper.vtfc import get_most_used_verbs, get_one_verb_conjugation
from scraper.export import export_to_sqlite

class TestVTFCScraper(unittest.TestCase):

    def test_headers_len(self):

        url = 'https://www.gymglish.com/fr/conjugaison/vatefaireconjuguer/verbe/etre'

        data = get_one_verb_conjugation(url, False)

        headers = ['Verb', 'Tense', 'Pronoun']

        self.assertRaises(Exception, export_to_sqlite, data, db_path=os.getcwd(), headers=headers)

    def test_first_fr_verb(self):

        url = 'https://www.gymglish.com/fr/conjugaison/vatefaireconjuguer/'

        data = get_most_used_verbs(url)

        self.assertEqual(list(data.keys())[0].lower(), 'être')

    def test_first_eng_verb(self):

        url = 'https://www.gymglish.com/fr/conjugaison/anglais'

        data = get_most_used_verbs(url)

        self.assertEqual(list(data.keys())[0].lower(), 'to be')


if __name__ == '__main__':

    unittest.main()