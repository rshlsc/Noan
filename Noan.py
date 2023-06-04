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
    file_handler.write_file(save_path.get(), deck)  # you need to check the correct way to save deck to a file

root = tk.Tk()
root.title("Noan")

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
