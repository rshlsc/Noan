#!/usr/bin/env python3
"""
Noan - Notion to Anki Converter
---
This script launches the modernized web-based version of Noan.
If you prefer the original simple interface, uncomment the 'launch_legacy_app' code below.
"""

import os
import sys
import webbrowser
import time
import subprocess

def launch_web_app():
    """Launch the new web-based Noan app"""
    print("Starting Noan Web App...")
    
    # Open the browser to the app URL
    webbrowser.open('http://localhost:3000')
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=3000)
    except ImportError:
        print("Error: Cannot import the new web app.")
        print("Make sure you have installed all dependencies with: pip install -r requirements.txt")
        sys.exit(1)

# Legacy app code - Uncomment if you prefer the original simple interface
"""
def launch_legacy_app():
    # Original Tkinter app
    import tkinter as tk
    from tkinter import filedialog, StringVar, Radiobutton
    import file_handler
    import markdown_parser
    import anki_generator

    def select_file():
        file_path.set(filedialog.askopenfilename())

    def save_file():
        save_path.set(filedialog.asksaveasfilename(defaultextension=".apkg"))

    def convert():
        content = file_handler.read_file(file_path.get())
        data = markdown_parser.parse(content, mode.get())
        deck = anki_generator.generate_anki_cards(data, mode.get())
        file_handler.write_file(save_path.get(), deck)

    root = tk.Tk()
    root.title("Noan (Legacy)")

    file_path = tk.StringVar()
    save_path = tk.StringVar()
    mode = tk.StringVar(value='anki_front_back')

    tk.Label(root, text="Select Markdown file:").pack()
    tk.Entry(root, textvariable=file_path).pack()
    tk.Button(root, text="Browse", command=select_file).pack()

    tk.Label(root, text="Save Anki file to:").pack()
    tk.Entry(root, textvariable=save_path).pack()
    tk.Button(root, text="Browse", command=save_file).pack()

    tk.Label(root, text="Conversion mode:").pack()
    Radiobutton(root, text="Anki Front and Back", variable=mode, value='anki_front_back').pack()
    Radiobutton(root, text="Anki Cloze Deletion", variable=mode, value='anki_cloze').pack()

    tk.Button(root, text="Convert", command=convert).pack()

    root.mainloop()
"""

if __name__ == "__main__":
    # Check if dependencies are installed
    try:
        import flask
        import genanki
    except ImportError:
        print("Required dependencies not found.")
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    
    # Launch the web app
    launch_web_app()
    
    # Uncomment to use the legacy app instead
    # launch_legacy_app()
