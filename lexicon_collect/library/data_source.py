# Lexicon project base data sources (word dictionaries)

import requests
import json


class DataSource:
    @staticmethod
    def query_merriam_webster_api(api_key: str, search_word: str) -> dict:
        url: str = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{search_word}'
        querystring: dict = {'key': api_key}
        headers: dict = {'Content-Type': 'application/json'}
        response = requests.request('GET', url, headers=headers, params=querystring)
        if response:
            package: dict = json.loads(response.text)
            return package
        else:
            print(f'Merriam Webster API Status code: {response}')
            return {}

    @staticmethod
    def query_oxford_api(app_id, app_key: str, search_word: str) -> dict:
        url: str = f'https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{search_word}'
        querystring: dict = {'strictMatch': 'false'}
        headers: dict = {
            'Content-Type': 'application/json',
            'app_id': app_id,
            'app_key': app_key
        }
        response = requests.request('GET', url, headers=headers, params=querystring)
        if response:
            package: dict = json.loads(response.text)
            # core_measurements: dict = package['data']['timelines'][0]['intervals']
            return package
        else:
            print(f'Oxford API Status code: {response}')
            return {}
