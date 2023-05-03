import re
import logging.config
from typing import Any, Union
from .data_source import DataSource
from .types.DictionaryResponseState import DictionaryResponseState
from .types.DictionaryError import DictionaryError
from .types.DictionaryApiResponse import DictionaryApiResponse
from .types.WebsterApiResponse import WebsterApiResponse
from .types.WebsterApiResponseNotFound import WebsterApiResponseNotFound


class LexiconCollect:
    __unavail_state: str = 'unavailable'
    __unavailable_definition: dict = {
        'state': __unavail_state,
        'spelling_suggestions': []
    }

    def __init__(self, webster_key: str, logging_object: Any):
        self._logger: logging.Logger = logging_object.getLogger(type(self).__name__)
        self._logger.setLevel(logging.INFO)
        self.webster_api_key = webster_key

    def get_merriam_webster_def(self, search_word: str) -> \
            Union[WebsterApiResponse, DictionaryError, WebsterApiResponseNotFound]:
        merriam_dictionary_response: list = DataSource.query_merriam_webster_api(self.webster_api_key, search_word)
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
                    if 'fl' in mw_subset:
                        part_of_speech = mw_subset['fl']
                    if 'prs' in mw_subset['hwi']:
                        pronounce = mw_subset['hwi']['prs'][0]['mw']
                    if 'hwi' in mw_subset:
                        word_break = mw_subset['hwi']['hw']
                    if 'shortdef' in mw_subset:
                        definition = mw_subset['shortdef']

                    merriam_response: WebsterApiResponse = {
                        'state': 'available',
                        'word_break': word_break,
                        'part_of_speech': part_of_speech,
                        'pronounce': pronounce,
                        'stems': stems,
                        'definition': definition,
                        'etymology': etymology,
                        'date_first_used': date
                    }
                    return merriam_response

                except KeyError as key_error:
                    self._logger.error(f'Received KeyError: {str(key_error)}')
                    return {'error': str(key_error)}
                except TypeError as type_error:
                    self._logger.error(f'Received TypeError: {str(type_error)}')
                    exit()
            elif type(merriam_dictionary_response) is list:
                return {
                    'state': self.__unavail_state,
                    'spelling_suggestions': merriam_dictionary_response
                }
            else:
                return self.__unavailable_definition
        else:
            return self.__unavailable_definition

    def get_dictionaryapi_def(self, search_word: str) -> \
            Union[DictionaryApiResponse, DictionaryError, DictionaryResponseState]:
        dictionaryapi_dictionary_response = DataSource.query_dictionaryapi(search_word)
        if dictionaryapi_dictionary_response and 'title' not in dictionaryapi_dictionary_response:
            try:
                dictionary_response: dict = dictionaryapi_dictionary_response[0]
                definition = ['n/a']
                example = audio_file = part_of_speech = pronounce = 'n/a'
                word = search_word

                if 'word' in dictionary_response:
                    word = dictionary_response['word']

                if 'phonetics' in dictionary_response and len(dictionary_response['phonetics']) > 0:
                    for phonetic in dictionary_response['phonetics']:
                        if 'text' in phonetic and 'audio' in phonetic:
                            pronounce = phonetic['text']
                            audio_file = phonetic['audio']
                            break

                if 'meanings' in dictionary_response and len(dictionary_response['meanings']) > 0:
                    for meaning in dictionary_response['meanings']:
                        temp_part_of_speech: str = ''

                        if 'partOfSpeech' in meaning:
                            if part_of_speech == 'n/a':
                                part_of_speech = ''
                            temp_part_of_speech = meaning['partOfSpeech']
                            part_of_speech = temp_part_of_speech if part_of_speech == '' \
                                else f'{part_of_speech}, {temp_part_of_speech}'

                        if 'definitions' in meaning and len(meaning['definitions']) > 0:
                            if definition[0] == 'n/a':
                                definition = []

                            for definition_container in meaning['definitions']:
                                part_of_speech_view = f'({temp_part_of_speech})' if temp_part_of_speech != '' else ''

                                if len(definition_container) > 0:
                                    definition.append(f'{definition_container["definition"]} {part_of_speech_view}')

                                if 'example' in definition_container and \
                                        len(definition_container['example']) >= len(example):
                                    example = definition_container['example']

                dictionaryapi_response: DictionaryApiResponse = {
                    'state': 'available',
                    'word': word,
                    'part_of_speech': part_of_speech,
                    'pronounce': pronounce,
                    'audio': audio_file,
                    'definition': definition,
                    'example': example
                }
                return dictionaryapi_response
            except KeyError as key_error:
                self._logger.error(f'Received TypeError (get_dictionaryapi_def): {str(key_error)}')
                return {'error': str(key_error)}
        else:
            return {'state': self.__unavail_state}
