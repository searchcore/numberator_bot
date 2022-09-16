from peewee import *
from pathlib import Path
import json
import random

BASE_DIR = Path(__file__).resolve().parent

db = SqliteDatabase(BASE_DIR/'phrases.db')

def init_table_from_json(path: str):
    """!DROPS! table and loads information from JSON file, specified in path.\
        JSON file must have layout such this:

        {
            'some_namespace': {
                'some_event_1': [
                    ['single message'],
                    ['some', 'text', 'sent in four different', 'messages'],
                    ['another message']
                ],
                'some_event_2': [
                    ['just single message and nothing more']
                ]
            }
            'another_namespace': ...\n
            ...
        }

        Messages for event will be randomly choosen from event's array.
        Each array in event variable contains text you want to send in different messages at once.

        You can use function get_phrase(name) to get messages text.
        Specify name using namespacename-doubleunderscore-eventname as follows:
        name = namespace__event

        """
    SchemaManager(Phrase, db).drop_table()
    Phrase.create_table()

    print('Loading phrases from JSON...')

    with open(path, 'r', encoding='utf8') as fp:
        json_phrases = json.load(fp)

        for namespace_name in json_phrases:
            for event_name in json_phrases[namespace_name]:
                events = json_phrases[namespace_name][event_name]

                for ev in events:
                    Phrase.create(name=f'{namespace_name}__{event_name}', list_text=ev)
    
    print('OK.')
    
def get_phrase(name : str, cache=False):
    """Returns phrases list from database with name 'name'.\
    If database contains several entries with same name, returns random one."""
    if cache:
        raise NotImplemented

    query = Phrase.select().where(Phrase.name == name)

    return random.choice(query).list_text

class PhraseTextField(Field):
    field_type = 'phrase'

    def db_value(self, value):
        assert isinstance(value, list), "Phrase must be list"
        for v in value:
            assert isinstance(v, str), "Phrase elements must be str"

        return json.dumps(value)

    def python_value(self, value):
        return json.loads(value)

class Phrase(Model):
    name = CharField()
    list_text = PhraseTextField()

    class Meta:
        database = db

if __name__ == '__main__':
    init_table_from_json(BASE_DIR/'cfg.json')