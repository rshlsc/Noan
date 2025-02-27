# Noan - Notion to Anki Converter

A modern web-based tool to convert Notion exports (both Markdown and HTML) to Anki flashcards.

![Noan Logo](https://img.shields.io/badge/Noan-Notion%20to%20Anki-6a11cb?style=for-the-badge)

## Features

- **Modern Web Interface**: Clean, intuitive UI for a seamless experience
- **Multiple File Formats**: Support for both Markdown (.md) and HTML exports from Notion
- **Multiple Card Types**: Create Basic, Cloze Deletion, and Basic-and-Reversed cards
- **ZIP Export Support**: Automatically handle Notion's ZIP exports
- **Preview Cards**: See how your cards will look before generating the deck
- **Custom Tags**: Add tags to better organize your Anki cards
- **Beautiful Card Styling**: Pre-styled cards for a better learning experience

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Step 1: Export Your Notion Page

#### For Markdown Export (Recommended)
1. In Notion, click the three dots (...) in the top-right corner of a page
2. Select "Export"
3. Choose "Markdown & CSV" as the export format
4. Click "Export"
5. You'll get a ZIP file - you can upload this directly to Noan!

#### For HTML Export
1. In Notion, click the three dots (...) in the top-right corner of a page
2. Select "Export"
3. Choose "HTML" as the export format
4. Click "Export"
5. You'll get a ZIP file - you can upload this directly to Noan!

### Step 2: Convert to Anki

1. Upload your Notion export to Noan
2. Configure your deck settings:
   - Choose your card type (Basic, Cloze, or Basic and Reversed)
   - Set a deck name
   - Add tags if desired
3. Preview your cards
4. Generate and download your Anki deck (.apkg file)

### Step 3: Import into Anki

1. Open Anki on your computer
2. Click "File" > "Import"
3. Select the .apkg file you downloaded
4. Your new deck is ready to use!

## Card Formatting

### Basic (Front → Back) Cards

In your Notion page, format your content like this:

```
- Question 
    - Answer
```

Or using toggle lists:

```
- Question
    - Answer with more details
```

### Cloze Deletion Cards

Format your cloze deletions in Notion like this:

```
The [capital] of France is (Paris).
```

- `[text]` becomes `{{c1::text}}`
- `(text)` becomes `{{c2::text}}`
- `{text}` becomes `{{c3::text}}`

### Basic and Reversed Cards

Use the same format as Basic cards, but both directions will be created:

```
- Term
    - Definition
```

This creates both "Term → Definition" and "Definition → Term" cards.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built with Flask, Bootstrap, and genanki
- Inspired by the original Noan tool
