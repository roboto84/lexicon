from lexicon.library.types.DictionaryDefinitionPackage import DictionaryDefinitionPackage

bind_def: DictionaryDefinitionPackage = {
    'word': 'bind',
    'date_first_used': 'before 12th century',
    'part_of_speech': 'verb',
    'word_break': 'bind',
    'pronounce': ["ˈbīnd", "bīnd"],
    'audio': 'https://audio.oxforddictionaries.com/en/mp3/bind__us_1.mp3',
    'etymology': 'Middle English, from Old English bindan; akin to Old High German '
                 'bintan to bind, Greek peisma cable, Sanskrit badhnāti he ties',
    'stems': [
        "bind",
        "binding",
        "binds",
        "bound",
        "bounded"
    ],
    'definitions': [
        "to make secure by tying",
        "to confine, restrain, or restrict as if with bonds",
        "to put under an obligation",
        "tie or fasten (something) tightly"
    ],
    'example': 'the logs were bound together with ropes'
}

initial_definitions: list[DictionaryDefinitionPackage] = [bind_def]
