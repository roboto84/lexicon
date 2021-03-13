import os
import sys
from dotenv import load_dotenv
from library.lexicon import Lexicon


def print_dictionary_results(dictionary_result: dict):
    if dictionary_result['merriam_webster']:
        mw_dictionary_def = dictionary_result['merriam_webster']
        print(f'------------------------------------')
        print(f'{mw_dictionary_def["word_break"]} ({mw_dictionary_def["part_of_speech"]}) '
              f'{mw_dictionary_def["date_first_used"]}')
        print(f'{mw_dictionary_def["pronounce"]}')
        print(f'Similar Words: {mw_dictionary_def["stems"]}')
        print(f'Definitions:')
        for position, definition in enumerate(mw_dictionary_def["definition"]):
            print(f'  {position}. {definition}')
        print(f'Etymology: {mw_dictionary_def["etymology"]}')

    if dictionary_result['oxford']:
        ox_dictionary_def = dictionary_result['oxford']
        print(f'------------------------------------')
        print(f'{ox_dictionary_def["word"]} ({ox_dictionary_def["part_of_speech"]})')
        print(f'{ox_dictionary_def["pronounce"]}')
        print(f'Audio: {ox_dictionary_def["audio"]}')
        print(f'Definitions:')
        for position, definition in enumerate(ox_dictionary_def["definition"]):
            print(f'  {position}. {definition}')
        print(f'Example Sentence: "{ox_dictionary_def["example"]}"')


if __name__ == '__main__':
    try:
        load_dotenv()
        MERRIAM_WEBSTER_API_KEY: str = os.getenv('MERRIAM_WEBSTER_API_KEY')
        OXFORD_APP_ID: str = os.getenv('OXFORD_APP_ID')
        OXFORD_APP_KEY: str = os.getenv('OXFORD_APP_KEY')

        if len(sys.argv) == 2:
            search_word = sys.argv[1]
            lexicon = Lexicon(MERRIAM_WEBSTER_API_KEY, OXFORD_APP_ID, OXFORD_APP_KEY)

            if not lexicon.spell_checker(search_word):
                print('The word provided seems to be misspelled.  Here are some suggestions...')
                for index, suggestion in enumerate(lexicon.spell_check_suggest(search_word)):
                    print(f'  {index}. {suggestion}')

            print(f'\nSearching...')
            print_dictionary_results(lexicon.get_dictionary_def(search_word))
        else:
            print('Please give a word to search')

    except TypeError as type_error:
        print(f'Received TypeError: Check that the .env project file is configured correctly: {type_error}')
        exit()
