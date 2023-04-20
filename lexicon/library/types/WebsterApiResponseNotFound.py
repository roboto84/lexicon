from typing import Union
from lexicon.library.types.DictionaryResponseState import DictionaryResponseState


class WebsterApiResponseNotFound(DictionaryResponseState):
    spelling_suggestions: list[str]
