
import enchant
from typing import List
from .lexicon_collect import LexiconCollect


class Lexicon:
    def __init__(self, webster_key: str, oxford_app_id: str, oxford_key: str):
        self.lexicon_collect = LexiconCollect(webster_key, oxford_app_id, oxford_key)
        self.enchant_dictionary = enchant.Dict('en_US')

    def spell_checker(self, word: str) -> bool:
        return self.enchant_dictionary.check(word)

    def spell_check_suggest(self, word: str) -> List[str]:
        return self.enchant_dictionary.suggest(word)

    def get_dictionary_def(self, search_word: str) -> dict:
        dictionary_payload: dict = {
            'search_word': search_word,
            'spelling_suggestions': [],
            'merriam_webster': self.lexicon_collect.get_merriam_webster_def(search_word),
            'oxford': self.lexicon_collect.get_oxford_def(search_word)
        }
        if dictionary_payload['merriam_webster']['state'] == 'unavailable':
            dictionary_payload['spelling_suggestions'] = [elem for elem in
                                                          dictionary_payload['merriam_webster']['spelling_suggestions']
                                                          if ' ' not in elem]
            del dictionary_payload['merriam_webster']['spelling_suggestions']
        else:
            dictionary_payload['merriam_webster']['stems'] = [elem for elem in
                                                              dictionary_payload['merriam_webster']['stems']
                                                              if ' ' not in elem]
        if not self.spell_checker(search_word):
            for index, suggestion in enumerate(self.spell_check_suggest(search_word)):
                if suggestion not in dictionary_payload['spelling_suggestions']:
                    dictionary_payload['spelling_suggestions'].append(suggestion)
        return dictionary_payload
