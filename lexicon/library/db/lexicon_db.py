
import logging.config
import os
from willow_core.library.sqlite_db import SqlLiteDb
from sqlite3 import Connection, Cursor, Error
from typing import Any, List, Optional


class LexiconDb(SqlLiteDb):
    def __init__(self, logging_object: Any, db_location: str):
        self._logger: logging.Logger = logging_object.getLogger(type(self).__name__)
        self._logger.setLevel(logging.INFO)
        super().__init__(logging_object, db_location)
        self._check_db_schema()

    @staticmethod
    def add_file_path(relative_file_path: str) -> str:
        return f'{os.path.dirname(__file__)}{relative_file_path}'

    def _check_db_schema(self) -> None:
        if self._check_db_state(['WORDS']):
            self._logger.info(f'DB schema looks good')
        else:
            self._logger.info(f'Tables not found')
            self._create_db_schema()

    def _create_db_schema(self) -> None:
        try:
            conn: Connection = self._db_connect()
            with open(self.add_file_path('/sql/schema.sql')) as f:
                conn.executescript(f.read())
            self._logger.info(f'Initializing Lexi_DB schema')
            self._db_close(conn)
            self._logger.info(f'Database has been initialized')
        except Error as error:
            self._logger.error(f'Error occurred initializing Lexi_DB: {str(error)}')

    def get_words(self, word_limit: Optional[int] = None) -> List[str]:
        try:
            sqlite_query: str = """select word_letter_cased from WORDS order by id desc"""
            if word_limit:
                sqlite_query: str = f'{sqlite_query} limit {word_limit}'
            conn: Connection = self._db_connect()
            db_cursor: Cursor = conn.cursor()
            db_words_result: List[list] = db_cursor.execute(sqlite_query).fetchall()
            self._logger.info(f'Retrieved words from Lexi_DB successfully')
            return [row[0] for row in db_words_result]
        except Error as error:
            self._logger.error(f'Error occurred getting words from Lexi_DB: {str(error)}')

    def get_random_word_def(self) -> dict:
        try:
            conn: Connection = self._db_connect()
            self.set_row_factory(conn)
            db_cursor: Cursor = conn.cursor()
            db_word_result: List[dict] = db_cursor.execute(
                """SELECT * FROM WORDS ORDER BY RANDOM() LIMIT 1;""").fetchall()
            if db_word_result and len(db_word_result) == 1:
                self._logger.info(f'Retrieved a random word from Lexi_DB successfully')
                return dict(db_word_result[0])
            else:
                self._logger.info(f'Random word index was not in Lexi_DB')
                return {}
        except Error as error:
            self._logger.error(f'Error occurred getting word a random word from Lexi_DB: {str(error)}')

    def get_word_from_db(self, search_word) -> dict:
        try:
            conn: Connection = self._db_connect()
            self.set_row_factory(conn)
            db_cursor: Cursor = conn.cursor()
            db_word_result: List[dict] = db_cursor.execute(
                """select * from WORDS where word_letter_cased is ?""", [search_word]).fetchall()
            if db_word_result and len(db_word_result) == 1:
                self._logger.info(f'Retrieved word "{search_word}" from Lexi_DB successfully')
                return dict(db_word_result[0])
            else:
                self._logger.info(f'Word "{search_word}" not in Lexi_DB')
                return {}
        except Error as error:
            self._logger.error(f'Error occurred getting word "{search_word}" from Lexi_DB: {str(error)}')

    def insert_word(self, def_data: dict) -> None:
        word: str = def_data['word']
        sql_path: str = self.add_file_path('/sql/insert_word.sql')
        conn: Connection = self._db_connect()
        db_cursor: Cursor = conn.cursor()
        table_list = db_cursor.execute("""SELECT word FROM WORDS WHERE word is ?;""", [word]).fetchall()

        if not table_list:
            try:
                self._logger.info(f'Inserting "{word}" into Lexicon_DB')
                with open(sql_path, 'r') as file:
                    db_cursor.execute(
                        file.read(),
                        (self._get_time(), word.lower(), word, def_data['date_first_used'], def_data['part_of_speech'],
                         def_data['word_break'], str(def_data['pronounce']), def_data['audio'],
                         str(def_data['etymology']), str(def_data['stems']), str(def_data['definitions']),
                         str(def_data['example'])))
            except IOError as io_error:
                self._logger.error(f'IOError was thrown: {str(io_error)}')
            except Exception as exception:
                self._logger.error(f'Exception was thrown: {str(exception)}')
        else:
            self._logger.info(f'"{word}" is already in the DB, not reinserting')
        self._db_close(conn)
