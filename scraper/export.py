import pandas as pd
import numpy as np
import json
import os
import sqlite3

from requests import head
sqlite3.register_adapter(np.int64, lambda val: int(val))
sqlite3.register_adapter(np.int32, lambda val: int(val))

def export_to_json(data, filepath) -> None:

    """
    Export data scraped from VTFC website to a json file

    ### Parameters
    1. data : dict
        - Dictionary containing the data scraped from VTFC website
    2. filepath : str
        - Directory where json file will be saved and the filename.json
    """

    with open(filepath + '.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=True)

def export_to_csv(data, filepath) -> None:

    """
    Export data scraped from VTFC website to a csv file

    ### Parameters
    1. data : dict
        - Dictionary containing the data scraped from VTFC website
    2. filepath : str
        - Directory where json file will be saved and the filename.csv
    """

    data_for_dataframe = list()

    for verb in list(data.keys()):
        for tense in list(data[verb].keys()):
            for conjugation in data[verb][tense]:
                data_for_dataframe.append([verb, tense, conjugation['pronoun'], conjugation['conjugated_verb']])

    df_most_used_verbs_conjungations = pd.DataFrame(data=data_for_dataframe, columns=['Verb', 'Tense', 'Pronoun', 'ConjugatedVerb'])


    df_most_used_verbs_conjungations.to_csv(filepath + '.csv', index=False)

def export_to_sqlite(data, db_path, db_name='ConjugationMostUsedVerbs.db', headers = ['Verb', 'Tense', 'Pronoun', 'Conjugated_verb']) -> None:

    """
    Export data scraped from VTFC website to a csv file

    ### Parameters
    1. data : dict
        - Dictionary containing the data scraped from VTFC website
    2. db_path : str
        - Directory where json file will be saved and the filename.csv
    3. db_name : str
        - SQLite database's name
    4. headers : list
        - List containing columnns headers
    """

    if len(headers) != 4:
        raise Exception('headers must receive a list with 4 elements')
    elif not all(isinstance(header, str) for header in headers):
        raise Exception('All elements of headers must be a str instance')

    data_for_dataframe = list()

    for verb in list(data.keys()):
        for tense in list(data[verb].keys()):
            for conjugation in data[verb][tense]:
                data_for_dataframe.append([verb, tense, conjugation['pronoun'], conjugation['conjugated_verb']])

    df_most_used_verbs_conjungations = pd.DataFrame(data=data_for_dataframe, columns=['Verb', 'Tense', 'Pronoun', 'ConjugatedVerb'])

    with sqlite3.connect(os.path.join(db_path, db_name)) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS ConjugatedVerbs (
                    {headers[0]} TEXT NOT NULL, 
                    {headers[1]} TEXT NOT NULL, 
                    {headers[2]} TEXT NOT NULL, 
                    {headers[3]} TEXT NOT NULL
                )
            """
        )
        cursor.executemany(
            f"""
                INSERT INTO ConjugatedVerbs (
                    {headers[0]}, 
                    {headers[1]}, 
                    {headers[2]}, 
                    {headers[3]}
                ) VALUIES (
                    ?, ?, ?, ?
                )
            """, 
            df_most_used_verbs_conjungations.to_records()
        )
        conn.commit()