import os
import sys
import logging.config
from dotenv import load_dotenv
from library.lexicon import Lexicon

if __name__ == '__main__':
    logging.config.fileConfig(fname=os.path.abspath('lexicon/bin/logging.conf'), disable_existing_loggers=False)
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    try:
        load_dotenv()
        MERRIAM_WEBSTER_API_KEY: str = os.getenv('MERRIAM_WEBSTER_API_KEY')
        OXFORD_APP_ID: str = os.getenv('OXFORD_APP_ID')
        OXFORD_APP_KEY: str = os.getenv('OXFORD_APP_KEY')
        SQL_LITE_DB: str = os.getenv('SQL_LITE_DB')

        if len(sys.argv) == 2:
            search_word = sys.argv[1]
            lexicon = Lexicon(MERRIAM_WEBSTER_API_KEY, OXFORD_APP_ID, OXFORD_APP_KEY, SQL_LITE_DB, logging)
            print(f'\nSearching...')
            print(lexicon.definition_summary(lexicon.get_definition(search_word)))
        else:
            print('Please give a word to search')

    except TypeError as type_error:
        print(f'Received TypeError: Check that the .env project file is configured correctly: {type_error}')
        exit()
