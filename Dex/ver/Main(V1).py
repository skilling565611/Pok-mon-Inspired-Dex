
import tkinter as tk
from tkinter import messagebox
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

# Center all content on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_left = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_left}+{position_top}')

center_window(root)

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
    info = f"ID: {monster['ID']}"
    info += f"Name: {monster['Dex_Name']}"
    info += f"Type: {monster['Type1']} {monster['Type2'] if monster['Type2'] else ''}"
    info += f"Abilities: {monster['Abilities']}"
    info += f"Moves: {monster['Moves']}"
    info += f"Description: {monster['Description']}"
    info += f"Games: {monster['Games']}"
    info_label.config(text=info)

# Function to create the list of monsters
def create_monster_list(monsters):
    for monster in monsters:
        button = tk.Button(root, text=monster['Dex_Name'], bg=Buttons_Color, fg=Buttons_Text_Color,
                           command=lambda m=monster: display_monster_info(m))
        button.pack(pady=5)

# Function to create and display the CSV and XML buttons
def create_game_buttons():
    for game in GAMES:
        game_button = tk.Button(root, text=game, bg=Buttons_Color, fg=Buttons_Text_Color,
                                command=lambda g=game: filter_monsters_by_game(g))
        game_button.pack(pady=10)

# Function to filter monsters by the selected game
def filter_monsters_by_game(game):
    filtered_monsters = [m for m in all_monsters if game in m['Games']]
    create_monster_list(filtered_monsters)

# Initialize the monster data (CSV and XML)
csv_file = 'monsters.csv'  # Your CSV file path
xml_file = 'monsters.xml'  # Your XML file path
all_monsters = load_csv_data(csv_file) + load_xml_data(xml_file)

# Create GUI elements
info_label = tk.Label(root, text="", bg=Background_Color, fg=Text_Color_Tittle, font=('Arial', 12), justify=tk.LEFT)
info_label.pack(pady=20)

# Create buttons to filter by games
create_game_buttons()

# Start the Tkinter main loop
root.mainloop()
