
import enchant
from typing import List
from lexicon_collect.library.lexicon_collect import LexiconCollect


class Lexicon:
    def __init__(self, webster_key: str, oxford_app_id: str, oxford_key: str):
        self.lexicon_collect = LexiconCollect(webster_key, oxford_app_id, oxford_key)
        self.enchant_dictionary = enchant.Dict('en_US')

    def spell_checker(self, word: str) -> bool:
        return self.enchant_dictionary.check(word)

    def spell_check_suggest(self, word: str) -> List[str]:
        return self.enchant_dictionary.suggest(word)

    def get_dictionary_def(self, search_word: str) -> dict:
        return {
            'merriam_webster': self.lexicon_collect.get_merriam_webster_def(search_word),
            'oxford': self.lexicon_collect.get_oxford_def(search_word)
        }
