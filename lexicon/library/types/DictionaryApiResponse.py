from typing import TypedDict


class DictionaryApiResponse(TypedDict):
    state: str
    word: str
    part_of_speech: str
    pronounce: str
    audio: str
    definition: list[str]
    example: str
