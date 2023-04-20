
import enchant
import logging.config
from typing import List, Any, Optional
from .lexicon_collect import LexiconCollect
from .lexicon_utils import LexiconUtils
from .db.lexicon_db import LexiconDb
from .types import WordDefinition


class Lexicon:
    def __init__(self, webster_key: str, oxford_app_id: str, oxford_key: str,
                 sql_lite_db_path: str, logging_object: Any):
        self._logger: logging.Logger = logging_object.getLogger(type(self).__name__)
        self._logger.setLevel(logging.INFO)
        self.lexicon_collect = LexiconCollect(webster_key, oxford_app_id, oxford_key, logging_object)
        self._lexicon_db = LexiconDb(logging_object, sql_lite_db_path)
        self.enchant_dictionary = enchant.Dict('en_US')

    @staticmethod
    def definition_summary(definition_data: dict) -> str:
        word_def_summary: str = 'Sorry, no information on that word was found.'

        if definition_data['definition_is_acceptable']:
            word_def_summary = LexiconUtils.definition_to_string(definition_data)
        elif 'spelling_suggestions' in definition_data and len(definition_data['spelling_suggestions']) > 0:
            word_def_chat_message = 'Looks like the word is misspelled. Perhaps try ...\n\n'
            spell_suggestions = ''.join(f'{spell_suggestion}, ' for spell_suggestion in
                                        definition_data['spelling_suggestions'])
            word_def_summary = f'{word_def_chat_message}{spell_suggestions}'.rstrip(',')
        return word_def_summary

    def spell_checker(self, word: str) -> bool:
        return self.enchant_dictionary.check(word)

    def spell_check_suggest(self, word: str) -> List[str]:
        return self.enchant_dictionary.suggest(word)

    def get_stored_words(self, word_limit: Optional[int] = None) -> List[str]:
        return self._lexicon_db.get_words(word_limit)

    def get_last_20_words(self) -> List[str]:
        return self._lexicon_db.get_words(20)

    def get_random_word_def(self) -> dict:
        return LexiconUtils.dictionary_data_from_db(
            self._lexicon_db.get_random_word_def()
        )

    def get_definition(self, search_word: str) -> dict:
        trimmed_search_word: str = search_word.strip()
        simple_definition_data: dict
        attempt_db_word_definition: dict = self._lexicon_db.get_word_from_db(trimmed_search_word)

        if attempt_db_word_definition:
            simple_definition_data = LexiconUtils.dictionary_data_from_db(attempt_db_word_definition)
            simple_definition_data['source'] = 'db'
        else:
            simple_definition_data = LexiconUtils.dictionary_data_from_api(
                self.get_dictionary_definitions(trimmed_search_word)
            )
            simple_definition_data['source'] = 'web'
            if simple_definition_data['definition_is_acceptable']:
                self._lexicon_db.insert_word(simple_definition_data)
        return simple_definition_data

    def get_dictionary_definitions(self, search_word: str) -> WordDefinition:
        try:
            trimmed_search_word: str = search_word.strip()
            dictionary_payload: WordDefinition = {
                'search_word': trimmed_search_word,
                'definition_is_acceptable': False,
                'spelling_suggestions': [],
                'merriam_webster': self.lexicon_collect.get_merriam_webster_def(trimmed_search_word),
                'oxford': self.lexicon_collect.get_dictionaryapi_def(trimmed_search_word)
            }
            dictionary_payload['definition_is_acceptable']: bool = LexiconUtils.definition_is_acceptable(
                dictionary_payload
            )

            if dictionary_payload['merriam_webster']['state'] == 'unavailable':
                dictionary_payload['spelling_suggestions'] = [
                    elem for elem in dictionary_payload['merriam_webster']['spelling_suggestions'] if ' ' not in elem
                ]
                del dictionary_payload['merriam_webster']['spelling_suggestions']
            else:
                dictionary_payload['merriam_webster']['stems'] = [
                    elem for elem in dictionary_payload['merriam_webster']['stems'] if ' ' not in elem
                ]
            if not self.spell_checker(trimmed_search_word):
                for index, suggestion in enumerate(self.spell_check_suggest(trimmed_search_word)):
                    if suggestion not in dictionary_payload['spelling_suggestions']:
                        dictionary_payload['spelling_suggestions'].append(suggestion)
            return dictionary_payload
        except KeyError as key_error:
            self._logger.error(f'Received KeyError (get_dictionary_definitions): {str(key_error)}')
            return {'error': str(key_error)}
