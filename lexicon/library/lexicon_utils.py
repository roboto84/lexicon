

class LexiconUtils:
    @staticmethod
    def definition_is_acceptable(data: dict) -> bool:
        webster_def_is_good = ('state' in data['merriam_webster'] and data['merriam_webster']['state'] != 'unavailable')
        oxford_def_is_good = ('state' in data['oxford'] and data['oxford']['state'] != 'unavailable')
        return webster_def_is_good or oxford_def_is_good

    @staticmethod
    def definition_to_string(data: dict) -> str:
        try:
            definition_string: str = ''.join(f'◦ {single_def}\n' for single_def in data['definitions'])
            word_pronunciations: str = ''.join(f'{pronunciation}, ' for pronunciation in data['pronounce']).rstrip(', ')
            stems: str = ''.join(f'{stem}, ' for stem in data['stems']).rstrip(', ')

            return f'\n📚  {data["word"].capitalize()} | {data["date_first_used"]} {data["part_of_speech"]}, ' \
                   f'{data["word_break"]} / {word_pronunciations} \n' \
                   f'{stems} \n' \
                   f'{data["audio"]} \n\n' \
                   f'etymology | {data["etymology"]} \n\n' \
                   f'{definition_string} \n' \
                   f'( ex | {data["example"].capitalize()} )'
        except TypeError as type_error:
            print(f'Received error (chat_message_builder): {str(type_error)}')

    @staticmethod
    def simple_dictionary_data(data: dict) -> dict:
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
            print(f'Received error (parse_dictionary_data): {str(type_error)}')
