from typing import Union
from lexicon.library.types.DictionaryResponseState import DictionaryResponseState


class WebsterApiResponse(DictionaryResponseState):
    word_break: str
    part_of_speech: str
    pronounce: str
    stems: list[str]
    definition: str
    etymology: Union[str, list[str]]
    date_first_used: str
