from typing import TypedDict, Union

from lexicon.library.types.DictionaryApiResponse import DictionaryApiResponse
from lexicon.library.types.DictionaryError import DictionaryError
from lexicon.library.types.DictionaryResponseState import DictionaryResponseState
from lexicon.library.types.WebsterApiResponse import WebsterApiResponse
from lexicon.library.types.WebsterApiResponseNotFound import WebsterApiResponseNotFound


class WordDefinition(TypedDict):
    search_word: str
    definition_is_acceptable: bool
    spelling_suggestions: list[str]
    merriam_webster: Union[WebsterApiResponse, DictionaryError, WebsterApiResponseNotFound]
    oxford: Union[DictionaryApiResponse, DictionaryError, DictionaryResponseState]
