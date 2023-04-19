
import ast


class LexiconUtils:
    @staticmethod
    def definition_is_acceptable(data: dict) -> bool:
        webster_def_is_good = ('state' in data['merriam_webster'] and data['merriam_webster']['state'] != 'unavailable')
        oxford_def_is_good = ('state' in data['oxford'] and data['oxford']['state'] != 'unavailable')
        return webster_def_is_good or oxford_def_is_good

    @staticmethod
    def term_view(term: str) -> str:
        return term if 'n/a' not in term.lower() and 'unk' not in term.lower() else ''

    @staticmethod
    def definition_to_string(data: dict) -> str:
        try:
            nl = '\n'
            definition_string: str = ''.join(f'◦ {single_def}\n' for single_def in data['definitions'])
            word_pronunciations: str = ''.join(
                f'{LexiconUtils.term_view(pronunciation)}, ' for pronunciation in data['pronounce']
            ).rstrip(', ')
            stems: str = ''.join(f'{stem}, ' for stem in data['stems']).rstrip(', ')

            return f'📚  {data["word"].capitalize()} | {LexiconUtils.term_view(data["date_first_used"])} ' \
                   f'{LexiconUtils.term_view(f"""{data["part_of_speech"]}, """)}' \
                   f'{LexiconUtils.term_view(data["word_break"])} / {word_pronunciations} ({data["source"]})\n' \
                   f'{stems}' \
                   f'{LexiconUtils.term_view(f"""{nl}{data["audio"]}""")}' \
                   f'{LexiconUtils.term_view(f"""{nl}{nl}etymology | {data["etymology"]}""")}' \
                   f'\n\n{definition_string}' \
                   f'{LexiconUtils.term_view(f"""{nl}( ex | {data["example"].capitalize()} ){nl}""")}'
        except TypeError as type_error:
            print(f'Received error (chat_message_builder): {str(type_error)}')

    @staticmethod
    def dictionary_data_from_db(data: dict) -> dict:
        try:
            if 'word' in data:
                return {
                    'word': data['word'],
                    'definition_is_acceptable': True,
                    'spelling_suggestions': [],
                    'stems': ast.literal_eval(data['stems']),
                    'date_first_used': data['date_first_used'],
                    'part_of_speech': data['part_of_speech'],
                    'word_break': data['word_break'],
                    'pronounce': ast.literal_eval(data['pronounce']),
                    'audio': data['audio'],
                    'etymology': data['etymology'],
                    'definitions': ast.literal_eval(data['definitions']),
                    'example': data['example']
                }
            else:
                return {}
        except TypeError as type_error:
            print(f'Received error (dictionary_data_from_db): {str(type_error)}')
        except KeyError as key_error:
            print(f'Received KeyError (dictionary_data_from_db): {str(key_error)}')

    @staticmethod
    def dictionary_data_from_api(data: dict) -> dict:
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
                part_of_speech = ox['part_of_speech'] if ('part_of_speech' in ox and len(ox['part_of_speech']) > 0) \
                    else part_of_speech
                pronounce.append((ox['pronounce'] if ('pronounce' in ox) else 'unk'))
                if 'definition' in ox and len(ox['definition']) > 0:
                    definitions = definitions + ox['definition']

            return {
                'word': data['search_word'],
                'definition_is_acceptable': data['definition_is_acceptable'],
                'spelling_suggestions': data['spelling_suggestions'],
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
            print(f'Received error (dictionary_data_from_api): {str(type_error)}')
        except KeyError as key_error:
            print(f'Received KeyError (dictionary_data_from_api): {str(key_error)}')
