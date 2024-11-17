
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
import os
import requests
from io import BytesIO


# Fix Alignment Issues
def center_widget(widget):
    widget.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (widget.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (widget.winfo_height() // 2)
    widget.geometry(f"+{x}+{y}")

# Automatically Check for Updates from GitHub
import requests

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/YourUsername/YourRepo/main/version.txt")
        response.raise_for_status()
        latest_version = response.text.strip()
        current_version = "1.0.0"  # Replace with your app's current version
        if latest_version != current_version:
            print(f"A new version ({latest_version}) is available. Please update!")
        else:
            print("You are using the latest version.")
    except Exception as e:
        print(f"Error checking for updates: {e}")

# Constants for the GUI
Background_Color = 'black'
Text_Color_Tittle = 'green'
Buttons_Color = 'dark blue'
Buttons_Text_Color = 'white'
Save_Background_Color = 'black'
Save_Text_Color = 'green'
Tittle = 'Pokémon-Inspired Dex'
DEBUG_MODE = False
Win_W, Win_H = 400, 504  # Default window size

# CSV columns
csv_columns = [
    "ID", "National{#}", "Monster_Name", "Type1", "Type2", "Abilities", 
    "Moves1", "Moves2", "Moves3", "Moves4", "HP", "Attack", "Defense", 
    "Speed", "IN Team", "IMG", "Game", "Generation"
]

# Setup the main window
root = tk.Tk()
root.title(Tittle)
root.geometry(f"{Win_W}x{Win_H}")  # Default window size
root.config(bg=Background_Color)

# Variables for entries and image
entries = {}
image_label = None  # Placeholder for the image widget
save_display = None  # Placeholder for the save display area

# Function to save data to CSV
def save_to_csv():
    global save_display

    # Collect data from input fields
    data = {key: entry.get() for key, entry in entries.items()}

    # Save to CSV
    csv_filename = "output.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerow(data)
    print(f"Data saved to {csv_filename}")

    # Clear input fields
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Update save display
    display_saved_data()

# Function to display the saved data at the bottom of the GUI
def display_saved_data():
    global save_display
    content = None
    csv_filename = "output.csv"

    # Read the CSV file to update the save area
    if os.path.exists(csv_filename):
        with open(csv_filename, "r") as file:
            content = file.read()

    # Update or create the save display
    if content:
        if save_display:
            save_display.config(state="normal")  # Make the area editable temporarily
            save_display.delete(1.0, tk.END)  # Clear existing content
            save_display.insert(tk.END, content)  # Insert new content
            save_display.config(state="disabled")  # Make it read-only again
        else:
            save_display = tk.Text(root, height=10, width=80, bg=Save_Background_Color, fg=Save_Text_Color, font=("Arial", 12))
            save_display.insert(tk.END, content)
            save_display.config(state="disabled")  # Make it read-only
            save_display.pack(side="bottom", pady=10)  # Place at the bottom of the GUI

# Function to load data from CSV but keep fields empty on startup
def load_csv_to_display():
    global save_display
    csv_filename = "output.csv"

    # Always clear input fields
    for entry in entries.values():
        entry.delete(0, tk.END)

    # Display save area content
    display_saved_data()

# Function to fetch and display an image from a URL
def display_image(image_url):
    global image_label
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check if the request was successful
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((150, 150), Image.ANTIALIAS)  # Resize image
        img_tk = ImageTk.PhotoImage(img)

        # Update or create the image label
        if image_label:
            image_label.config(image=img_tk)
            image_label.image = img_tk
        else:
            image_label = tk.Label(content_frame, image=img_tk, bg=Background_Color)
            image_label.image = img_tk
            image_label.pack(pady=10)
    except Exception as e:
        print(f"Error fetching image from {image_url}: {e}")
        if image_label:
            image_label.pack_forget()  # Hide the image label if the image can't be fetched

# Create a main frame to hold the canvas and scrollbars
main_frame = tk.Frame(root, bg=Background_Color)
main_frame.pack(fill="both", expand=True)

# Create a canvas for scrolling
canvas = tk.Canvas(main_frame, bg=Background_Color, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# Touch support for scrolling
def start_touch_scroll(event):
    canvas.scan_mark(event.x, event.y)  # Mark the starting point of the touch

def touch_scroll(event):
    canvas.scan_dragto(event.x, event.y, gain=1)  # Drag the canvas as the user moves

# Bind touch events
canvas.bind("<ButtonPress-1>", start_touch_scroll)  # Touch press
canvas.bind("<B1-Motion>", touch_scroll)  # Touch drag

# Create a canvas for scrolling
canvas = tk.Canvas(main_frame, bg=Background_Color, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# Touch support for scrolling
def start_touch_scroll(event):
    canvas.scan_mark(event.x, event.y)  # Mark the starting point of the touch

def touch_scroll(event):
    canvas.scan_dragto(event.x, event.y, gain=1)  # Drag the canvas as the user moves

# Bind touch events
canvas.bind("<ButtonPress-1>", start_touch_scroll)  # Touch press
canvas.bind("<B1-Motion>", touch_scroll)  # Touch drag

# Create scrollbars
v_scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, width=16)
v_scrollbar.pack(side="right", fill="y")

h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview, width=16)
h_scrollbar.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Create a frame inside the canvas to hold all content
content_frame = tk.Frame(canvas, bg=Background_Color)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Update the scroll region when the frame size changes
def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", configure_scroll_region)

# Title Label
title_label = tk.Label(content_frame, text=Tittle, bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 18, "bold"))
title_label.pack(pady=20)

# Function to move to the next entry on "Enter" and auto-scroll
def move_to_next_entry(event, current_index):
    next_index = current_index + 1
    if next_index < len(csv_columns):  # Ensure within bounds
        next_key = csv_columns[next_index]
        next_entry = entries[next_key]
        next_entry.focus_set()  # Move focus to the next entry

        # Auto-scroll if the next entry is out of view
        entry_y = next_entry.winfo_rooty() - canvas.winfo_rooty()  # Position relative to canvas
        entry_height = next_entry.winfo_height()

        if entry_y + entry_height > canvas.winfo_height():  # Entry is below the visible area
            canvas.yview_scroll(1, "units")  # Scroll down
        elif entry_y < 0:  # Entry is above the visible area
            canvas.yview_scroll(-1, "units")  # Scroll up

# Monster Creation Input Fields
for index, column in enumerate(csv_columns):
    label = tk.Label(content_frame, text=column, bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 12))
    label.pack(pady=2)

    entry = tk.Entry(content_frame, bg="white", fg="black", font=("Arial", 12))
    entry.pack(pady=2)
    entry.bind("<Return>", lambda event, idx=index: move_to_next_entry(event, idx))  # Bind "Enter" key
    entries[column] = entry

# Save button (saves to CSV)
save_button = tk.Button(content_frame, text="Save", command=save_to_csv, bg=Buttons_Color, fg=Buttons_Text_Color, font=("Arial", 12))
save_button.pack(pady=10)

# Keyboard Bindings for Scrolling
def scroll_canvas(event):
    if event.keysym == "Up":
        canvas.yview_scroll(-1, "units")
    elif event.keysym == "Down":
        canvas.yview_scroll(1, "units")
    elif event.keysym == "Left":
        canvas.xview_scroll(-1, "units")
    elif event.keysym == "Right":
        canvas.xview_scroll(1, "units")

# Bind Arrow Keys to Scroll
root.bind("<Up>", scroll_canvas)
root.bind("<Down>", scroll_canvas)
root.bind("<Left>", scroll_canvas)
root.bind("<Right>", scroll_canvas)

# Load data from CSV to display save area on startup
load_csv_to_display()

# Start the application
root.mainloop()
