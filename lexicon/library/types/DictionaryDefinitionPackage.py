from typing import TypedDict


class DictionaryDefinitionPackage(TypedDict):
    word: str
    date_first_used: str
    part_of_speech: str
    word_break: str
    pronounce: list[str]
    audio: str
    etymology: str
    stems: list[str]
    definitions: list[str]
    example: str
