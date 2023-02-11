<h1 align="center">lexicon</h1>

<div align="center">
	<img src="assets/lexicon.png" width="250" title="lexicon logo">
</div>

## About
`lexicon` is a command line and lib toolset for word definitions, spell check, and spelling suggestions with SQLite data support.

## Install
This project is managed with [Python Poetry](https://github.com/python-poetry/poetry). With Poetry installed correctly, simply clone this project and install its dependencies:

- Clone repo
    ```
    git clone https://github.com/roboto84/lexicon.git
    ```
    ```
    cd lexicon
    ```
- Install dependencies
    ```
    poetry install
    ```

## API Keys
Before you begin with `lexicon` you first need a dictionary API key.

- Merriam-Webster Dictionary (Required) - https://dictionaryapi.com
- Oxford Dictory (Optional) - https://developer.oxforddictionaries.com

## Environmental Variables
`lexicon` requires that an `.env` file is available in the *same* directory it is running under.

- The format of the `.env` file should contain the following as defined environmental variables:
    - `MERRIAM_WEBSTER_API_KEY` : Key obtained in the previous step.
    - `OXFORD_APP_ID` : Optional. Oxford App ID obtained in the previous step.
    - `OXFORD_APP_KEY` : Optional. Oxford App Key obtained in the previous step.
    - `SQL_LITE_DB`: Location of Lexicon SQLite DB.

- An explained `.env` file format is shown below:
    ```
    MERRIAM_WEBSTER_API_KEY=<Merriam Webster API Key>
    OXFORD_APP_ID=<Oxford App ID>
    OXFORD_APP_KEY=<Oxford App Key>
    SQL_LITE_DB=<Lexicon DB Location>
    ```

- A typical `.env` file may look like this:
    ```
    MERRIAM_WEBSTER_API_KEY=9d1e4882-x649-20f4-34h5-7eole23fe931
    OXFORD_APP_ID=72f1j384
    OXFORD_APP_KEY=rofdw34h65h33grw73589f3ss2g11fg02
    SQL_LITE_DB=/home/data/lexicon.db
    ```

## Usage
- Run the script once the environment (`.env`) file is created:
    ```
    poetry run python lexicon/main.py <word to search>
    ```

## Example
```
poetry run python lexicon/main.py hello
```
```
📚  Hello | 1834 noun, hel*lo / hə-ˈlō (web)
hello, hellos

etymology | alteration of hollo

◦ an expression or gesture of greeting —used interjectionally in greeting, in answering the telephone, or to express surprise
```


## Commit Conventions
Git commits follow [Conventional Commits](https://www.conventionalcommits.org) message style as explained in detail on their website.

<br/>
<sup>
    <a href="https://www.flaticon.com/free-icons/dictionary" title="dictionary icons">
        lexicon icon created by Freepik - Flaticon
    </a>
</sup>


