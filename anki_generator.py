import genanki
import re

def generate_anki_cards(data, mode):
    my_deck = genanki.Deck(2059400110, 'My Deck')

    if mode == 'anki_front_back':
        my_model = genanki.Model(
            1607392319,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Question}}',
                    'afmt': '{{Answer}}',
                },
            ])

        for front, back in data:
            my_deck.add_note(genanki.Note(
                model=my_model,
                fields=[front, back]))

    elif mode == 'anki_cloze':
        my_model = genanki.Model(
            1607392320,
            'Cloze Model',
            fields=[
                {'name': 'Text'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{cloze:Text}}',
                    'afmt': '{{cloze:Text}}',
                },
            ],
            model_type=genanki.Model.CLOZE)

        for i, text in enumerate(data, start=1):
            print(text)  # Add this line to see what 'text' looks like

            cloze_text = text
            for j, match in enumerate(re.findall(r'\[.*?\]|\(.*?\)', text), start=1):
                cloze_text = cloze_text.replace(match, '{{c' + str(j) + '::' + match[1:-1] + '}}', 1)

            # Add a unique identifier to each card
            unique_id = '\u200B' * i
            cloze_text += unique_id

            my_deck.add_note(genanki.Note(
                model=my_model,
                fields=[cloze_text]))


    return my_deck
