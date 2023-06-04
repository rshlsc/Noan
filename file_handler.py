# file_handler.py
import genanki

def read_file(path):
    with open(path) as file:
        return file.read()

def write_file(path, deck):
    package = genanki.Package(deck)
    package.write_to_file(path)
