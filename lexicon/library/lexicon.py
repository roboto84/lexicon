
import enchant
from typing import List
from .lexicon_collect import LexiconCollect


class Lexicon:
    def __init__(self, webster_key: str, oxford_app_id: str, oxford_key: str):
        self.lexicon_collect = LexiconCollect(webster_key, oxford_app_id, oxford_key)
        self.enchant_dictionary = enchant.Dict('en_US')

    @staticmethod
    def definition_is_acceptable(data: dict) -> bool:
        webster_def_is_good = ('state' in data['merriam_webster'] and data['merriam_webster']['state'] != 'unavailable')
        oxford_def_is_good = ('state' in data['oxford'] and data['oxford']['state'] != 'unavailable')
        return webster_def_is_good or oxford_def_is_good

    @staticmethod
    def parse_dictionary_data(data: dict) -> dict:
        date_first_used: str = ''
        part_of_speech: str = ''
        word_break: str = ''
        pronounce: list[str] = []
        stems: list[str] = []
        audio: str = ''
        etymology: str = ''
        definitions: list[str] = []
        example: str = ''

        try:
            if 'merriam_webster' in data:
                mw = data['merriam_webster']
                date_first_used = mw['date_first_used'] if ('date_first_used' in mw) else 'unk'
                part_of_speech = mw['part_of_speech'] if ('part_of_speech' in mw) else 'unk'
                word_break = mw['word_break'] if ('word_break' in mw) else 'unk'
                stems = mw['stems'] if ('stems' in mw) else []
                pronounce.append((mw['pronounce'] if ('pronounce' in mw) else 'unk'))
                etymology = mw['etymology'] if ('etymology' in mw) else 'unk'
                if 'definition' in mw and len(mw['definition']) > 0:
                    definitions = mw['definition']

            if 'oxford' in data:
                ox = data['oxford']
                audio = ox['audio'] if ('audio' in ox) else 'unk'
                example = ox['example'] if ('example' in ox) else 'unk'
                pronounce.append((ox['pronounce'] if ('pronounce' in ox) else 'unk'))
                if 'definition' in ox and len(ox['definition']) > 0:
                    definitions = definitions + ox['definition']

            return {
                'word': data["search_word"],
                'stems': stems,
                'date_first_used': date_first_used,
                'part_of_speech': part_of_speech,
                'word_break': word_break,
                'pronounce': pronounce,
                'audio': audio,
                'etymology': etymology,
                'definitions': definitions,
                'example': example
            }
        except TypeError as type_error:
            print(f'Received error (parse_dictionary_data): {str(type_error)}')

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
