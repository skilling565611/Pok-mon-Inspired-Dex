import tkinter as tk
from tkinter import ttk
import csv
import xml.etree.ElementTree as ET

# Constants for the GUI
Background_Color = 'black'
Text_Color_Tittle = 'green'
Win_W = 800
Win_H = 600
IMG_Win_W = 400
IMG_Win_H = 400
Tittle = 'Pokémon-Inspired Dex'
Buttons_Color = 'dark blue'
Buttons_Text_Color = 'red'
DEBUG_MODE = False

# Sample Data for Games (can be extended or modified)
GAMES = ["Mystic Beasts", "Elemental Clash", "Legends of Terra"]

# Setup the main window
root = tk.Tk()
root.title(Tittle)
root.geometry(f'{Win_W}x{Win_H}')
root.config(bg=Background_Color)

# Create a canvas and scroll bar for scrolling
canvas = tk.Canvas(root, bg=Background_Color)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.config(yscrollcommand=scrollbar.set)

# Create a frame to hold all the content that needs scrolling
scrollable_frame = tk.Frame(canvas, bg=Background_Color)

# Add the scrollable frame to the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Title label
title_label = tk.Label(scrollable_frame, text=Tittle, bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 18, 'bold'))
title_label.pack(pady=10)

# Dropdown Menu for Game Group (Editable)
def on_game_group_select(event):
    selected_game_group = game_group_combobox.get()
    print(f"Selected Game Group: {selected_game_group}")

game_group_label = tk.Label(scrollable_frame, text="Select or Add Game Group:", bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 14))
game_group_label.pack(pady=5)

game_group_combobox = ttk.Combobox(scrollable_frame, values=GAMES, state="normal", width=20)  # Editable dropdown
game_group_combobox.set(GAMES[0])  # Default to the first game in the list
game_group_combobox.bind("<<ComboboxSelected>>", on_game_group_select)
game_group_combobox.pack(pady=10)

# Monster Creation Section
monster_creation_label = tk.Label(scrollable_frame, text="Monster Creation", bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 16, 'bold'))
monster_creation_label.pack(pady=10)

# List of CSV Columns (First Row)
csv_columns = ["ID", "Dex_Name", "Type1", "Type2", "Abilities", "Moves", "Description", "Games"]

# Dictionary to store the Entry widgets
entry_widgets = {}

# Create a frame to hold each label and entry widget vertically
for column in csv_columns:
    # Create a frame for each label-entry pair
    frame = tk.Frame(scrollable_frame, bg=Background_Color)
    frame.pack(fill='x', pady=5)  # Each frame will fill horizontally

    # Create a label for each field
    label = tk.Label(frame, text=column, bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 12))
    label.pack(side='left', padx=10)

    # Create an entry box for each field
    entry = tk.Entry(frame, bg="white", fg="black", font=('Arial', 12))
    entry.pack(side='right', padx=10, fill='x', expand=True)

    # Store the entry widget in the dictionary with the column name as key
    entry_widgets[column] = entry

# Function to load data from CSV
def load_csv_data(filename):
    monsters = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            monsters.append(row)
    return monsters

# Function to load data from XML
def load_xml_data(filename):
    monsters = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for monster in root.findall('monster'):
        monsters.append({
            'ID': monster.find('ID').text,
            'Dex_Name': monster.find('Dex_Name').text,
            'Type1': monster.find('Type1').text,
            'Type2': monster.find('Type2').text,
            'Abilities': monster.find('Abilities').text,
            'Moves': monster.find('Moves').text,
            'Description': monster.find('Description').text,
            'Games': monster.find('Games').text,
        })
    return monsters

# Function to display monsters in the GUI
def display_monster_info(monster):
    info = f"ID: {monster['ID']}\n"
    info += f"Name: {monster['Dex_Name']}\n"
    info += f"Type: {monster['Type1']} {monster['Type2'] if monster['Type2'] else ''}\n"
    info += f"Abilities: {monster['Abilities']}\n"
    info += f"Moves: {monster['Moves']}\n"
    info += f"Description: {monster['Description']}\n"
    info += f"Games: {monster['Games']}\n"
    info_label.config(text=info)

# Initialize the monster data (CSV and XML)
csv_file = 'monsters.csv'  # Your CSV file path
xml_file = 'monsters.xml'  # Your XML file path
all_monsters = load_csv_data(csv_file) + load_xml_data(xml_file)

# Create GUI elements
info_label = tk.Label(scrollable_frame, text="", bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 12), justify=tk.LEFT)
info_label.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
