import genanki
import re
import html
import logging
import random
import time
import os

logger = logging.getLogger(__name__)

# Define default Anki models (note types)
BASIC_MODEL = genanki.Model(
    1607392319,
    'Noan Basic',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
        {
            'name': 'Card',
            'qfmt': '<div class="question">{{Question}}</div>',
            'afmt': '<div class="question">{{Question}}</div><hr id="answer"><div class="answer">{{Answer}}</div>',
        },
    ],
    css='''
    .card {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18px;
        text-align: left;
        color: #333;
        background-color: #f5f5f5;
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    .question {
        font-weight: bold;
        font-size: 20px;
        color: #2c3e50;
    }
    .answer {
        margin-top: 10px;
        color: #27ae60;
    }
    '''
)

BASIC_AND_REVERSED_MODEL = genanki.Model(
    1607392320,
    'Noan Basic and Reversed',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '<div class="front">{{Front}}</div>',
            'afmt': '<div class="front">{{Front}}</div><hr id="answer"><div class="back">{{Back}}</div>',
        },
        {
            'name': 'Card 2',
            'qfmt': '<div class="front">{{Back}}</div>',
            'afmt': '<div class="front">{{Back}}</div><hr id="answer"><div class="back">{{Front}}</div>',
        },
    ],
    css='''
    .card {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18px;
        text-align: left;
        color: #333;
        background-color: #f5f5f5;
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    .front {
        font-weight: bold;
        font-size: 20px;
        color: #2c3e50;
    }
    .back {
        margin-top: 10px;
        color: #27ae60;
    }
    '''
)

CLOZE_MODEL = genanki.Model(
    1607392321,
    'Noan Cloze',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
    ],
    templates=[
        {
            'name': 'Cloze',
            'qfmt': '<div class="cloze">{{cloze:Text}}</div>{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}',
            'afmt': '<div class="cloze">{{cloze:Text}}</div>{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}',
        },
    ],
    css='''
    .card {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 18px;
        text-align: left;
        color: #333;
        background-color: #f5f5f5;
        padding: 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    .cloze {
        font-weight: normal;
        color: #2c3e50;
    }
    .cloze-deletion {
        font-weight: bold;
        color: #3498db;
    }
    .extra {
        margin-top: 20px;
        color: #7f8c8d;
        font-style: italic;
        border-top: 1px solid #ddd;
        padding-top: 10px;
    }
    ''',
    model_type=genanki.Model.CLOZE
)

class NoAnNote(genanki.Note):
    """Custom Note class with deterministic GUID generation"""
    
    @property
    def guid(self):
        """Generate a deterministic GUID from note content"""
        # Use first field as primary identifier
        content = self.fields[0]
        # Add timestamp to make it unique
        unique_id = f"{content}_{int(time.time())}"
        return genanki.guid_for(unique_id)

def generate_anki_cards(data, mode, options=None):
    """
    Generate Anki cards based on parsed data
    
    Args:
        data: Parsed data from markdown_parser
        mode: Card generation mode
        options: Additional options for card generation
        
    Returns:
        Generated Anki deck
    """
    if options is None:
        options = {}
    
    # Get deck options
    deck_name = options.get('deck_name', 'My Deck')
    deck_id = options.get('deck_id', random.randrange(1 << 30, 1 << 31))
    tags = options.get('tags', [])
    
    # Create deck
    my_deck = genanki.Deck(deck_id, deck_name)
    
    if mode == 'anki_front_back':
        _generate_front_back_cards(my_deck, data, tags, options)
    elif mode == 'anki_cloze':
        _generate_cloze_cards(my_deck, data, tags, options)
    elif mode == 'anki_basic_and_reversed':
        _generate_basic_and_reversed_cards(my_deck, data, tags, options)
    else:
        logger.warning(f"Unknown card generation mode: {mode}, falling back to front_back")
        _generate_front_back_cards(my_deck, data, tags, options)
    
    return my_deck

def _generate_front_back_cards(deck, data, tags, options):
    """Generate basic front/back cards"""
    for front, back in data:
        # Create a note and add it to the deck
        my_note = NoAnNote(
            model=BASIC_MODEL,
            fields=[front, back],
            tags=tags
        )
        deck.add_note(my_note)

def _generate_cloze_cards(deck, data, tags, options):
    """Generate cloze deletion cards"""
    for text in data:
        # Add extra field if specified
        extra = options.get('extra', '')
        
        my_note = NoAnNote(
            model=CLOZE_MODEL,
            fields=[text, extra],
            tags=tags
        )
        deck.add_note(my_note)

def _generate_basic_and_reversed_cards(deck, data, tags, options):
    """Generate basic cards with forward and reverse directions"""
    for front, back in data:
        my_note = NoAnNote(
            model=BASIC_AND_REVERSED_MODEL,
            fields=[front, back],
            tags=tags
        )
        deck.add_note(my_note)
