
import re
from .data_source import DataSource


class LexiconCollect:
    def __init__(self, webster_key: str, oxford_app_id: str, oxford_key: str):
        self.webster_api_key = webster_key
        self.oxford_app_id = oxford_app_id
        self.oxford_key = oxford_key

    def get_merriam_webster_def(self, search_word: str) -> dict:
        merriam_dictionary_response = DataSource.query_merriam_webster_api(self.webster_api_key, search_word)
        if merriam_dictionary_response:
            if type(merriam_dictionary_response[0]) is dict:
                try:
                    mw_subset = merriam_dictionary_response[0]
                    uros_word_break = uros_pronounce = date = part_of_speech = 'n/a'
                    definition = pronounce = word_break = 'n/a'
                    stems = etymology = ['n/a']

                    if 'stems' in mw_subset['meta']:
                        stems = mw_subset['meta']['stems']
                    if 'date' in mw_subset:
                        date = re.sub('{.*?}', '', mw_subset['date'])
                    if 'et' in mw_subset:
                        etymology = re.sub('{.*?}', '', mw_subset['et'][0][1])
                    if 'uros' in mw_subset:
                        uros_word_break = mw_subset['uros'][0]['ure']
                        if 'prs' in mw_subset['uros'][0]:
                            uros_pronounce = mw_subset['uros'][0]['prs'][0]['mw']
                    if 'fl' in mw_subset:
                        part_of_speech = mw_subset['fl']
                    if 'prs' in mw_subset['hwi']:
                        pronounce = mw_subset['hwi']['prs'][0]['mw']
                    if 'hwi' in mw_subset:
                        word_break = mw_subset['hwi']['hw']
                    if 'shortdef' in mw_subset:
                        definition = mw_subset['shortdef']

                    merriam_response = {
                        'word_break': word_break,
                        'part_of_speech': part_of_speech,
                        'pronounce': pronounce,
                        'stems': stems,
                        'definition': definition,
                        'etymology': etymology,
                        'date_first_used': date,
                        'sub_words': {
                            'word_break': uros_word_break,
                            'pronounce': uros_pronounce,
                            'part_of_speech': part_of_speech,
                        }
                    }
                    return merriam_response

                except KeyError as key_error:
                    print(f'Received TypeError: {key_error}')
                    return {'error': str(key_error)}
                except TypeError as type_error:
                    print(f'Received TypeError: {type_error}')
                    exit()
        else:
            return merriam_dictionary_response

    def get_oxford_def(self, search_word: str) -> dict:
        oxford_dictionary_response = DataSource.query_oxford_api(self.oxford_app_id, self.oxford_key, search_word)
        if oxford_dictionary_response:
            try:
                ox_subset = oxford_dictionary_response['results'][0]
                ox_lex_ent_subset = ox_subset['lexicalEntries'][0]
                definition = ['n/a']
                example = audio_file = part_of_speech = pronounce = 'n/a'
                word = search_word

                if 'word' in oxford_dictionary_response:
                    word = oxford_dictionary_response['word']
                if 'text' in ox_lex_ent_subset['lexicalCategory']:
                    part_of_speech = ox_lex_ent_subset['lexicalCategory']['text']
                if 'pronunciations' in ox_lex_ent_subset['entries'][0]:
                    pronounce = ox_lex_ent_subset['entries'][0]['pronunciations'][0]['phoneticSpelling']
                if 'definitions' in ox_lex_ent_subset['entries'][0]['senses'][0]:
                    definition = ox_lex_ent_subset['entries'][0]['senses'][0]['definitions']
                if 'examples' in ox_lex_ent_subset['entries'][0]['senses'][0]:
                    example = ox_lex_ent_subset['entries'][0]['senses'][0]['examples'][0]['text']
                if 'audioFile' in ox_lex_ent_subset['entries'][0]['pronunciations'][1]:
                    audio_file = ox_lex_ent_subset['entries'][0]['pronunciations'][1]['audioFile']

                oxford_response = {
                    'word': word,
                    'part_of_speech': part_of_speech,
                    'pronounce': pronounce,
                    'audio': audio_file,
                    'definition': definition,
                    'example': example
                }
                return oxford_response
            except KeyError as key_error:
                print(f'Received TypeError: {key_error}')
                return {'error': str(key_error)}
        else:
            return oxford_dictionary_response
