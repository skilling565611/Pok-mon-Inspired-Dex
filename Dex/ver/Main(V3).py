import tkinter as tk
from tkinter import ttk

# Constants for the GUI
Background_Color = 'black'
Text_Color_Tittle = 'green'
Win_W, Win_H = 400, 504
Tittle = 'Pokémon-Inspired Dex'

# Sample Data for Games (can be extended or modified)
GAMES = ["Mystic Beasts", "Elemental Clash", "Legends of Terra"]

# Setup the main window
root = tk.Tk()
root.title(Tittle)
root.geometry(f'{Win_W}x{Win_H}')
root.config(bg=Background_Color)

# Function to update the window size label
def update_window_size():
    width = root.winfo_width()
    height = root.winfo_height()
    size_label.config(text=f"{width}x{height}")
    root.after(500, update_window_size)  # Update every 500ms

# Create a main frame to hold the canvas and scrollbars
main_frame = tk.Frame(root, bg=Background_Color)
main_frame.pack(fill="both", expand=True)

# Create a canvas for scrolling
canvas = tk.Canvas(main_frame, bg=Background_Color, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

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

# Mouse scroll support for global scrolling
def on_mouse_scroll(event):
    if event.delta:  # For Windows (delta values)
        if event.state == 0:  # Vertical scrolling
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.state == 1:  # Horizontal scrolling (Shift + mouse wheel)
            canvas.xview_scroll(-1 * (event.delta // 120), "units")
    else:  # For macOS/Linux (event.num is used)
        if event.num == 4:  # Scroll up
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            canvas.yview_scroll(1, "units")

# Keybinds for navigation
def scroll_up(event=None):
    canvas.yview_scroll(-1, "units")  # Scroll up

def scroll_down(event=None):
    canvas.yview_scroll(1, "units")  # Scroll down

def scroll_left(event=None):
    canvas.xview_scroll(-1, "units")  # Scroll left

def scroll_right(event=None):
    canvas.xview_scroll(1, "units")  # Scroll right

def scroll_to_top(event=None):
    canvas.yview_moveto(0)  # Move to the top

def scroll_to_bottom(event=None):
    canvas.yview_moveto(1)  # Move to the bottom

# Bind mouse and key events to the root window for global scrolling
root.bind_all("<MouseWheel>", on_mouse_scroll)  # Windows: Mouse wheel
root.bind_all("<Shift-MouseWheel>", on_mouse_scroll)  # Horizontal scrolling with Shift
root.bind_all("<Button-4>", on_mouse_scroll)  # macOS/Linux scroll up
root.bind_all("<Button-5>", on_mouse_scroll)  # macOS/Linux scroll down
root.bind("<Up>", scroll_up)  # Arrow Up
root.bind("<Down>", scroll_down)  # Arrow Down
root.bind("<Left>", scroll_left)  # Arrow Left
root.bind("<Right>", scroll_right)  # Arrow Right
root.bind("<Home>", scroll_to_top)  # Home key
root.bind("<End>", scroll_to_bottom)  # End key

# Title Label
title_label = tk.Label(content_frame, text=Tittle, bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 18, "bold"))
title_label.pack(pady=20)

# Dropdown Menu
game_group_label = tk.Label(content_frame, text="Select or Add Game Group:", bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 14))
game_group_label.pack(pady=10)

game_group_combobox = ttk.Combobox(content_frame, values=GAMES, state="normal", width=20)
game_group_combobox.set(GAMES[0])
game_group_combobox.pack(pady=5)

# Monster Creation Section
monster_creation_label = tk.Label(content_frame, text="Monster Creation", bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 16, "bold"))
monster_creation_label.pack(pady=20)

# Monster Creation Input Fields
csv_columns = ["ID", "Dex_Name", "Type1", "Type2", "Abilities", "Moves", "Description", "Games"]
for column in csv_columns:
    label = tk.Label(content_frame, text=column, bg=Background_Color, fg=Text_Color_Tittle, font=("Arial", 12))
    label.pack(pady=2)

    entry = tk.Entry(content_frame, bg="white", fg="black", font=("Arial", 12))
    entry.pack(pady=2)

# Temporary Window Size Display in Top-Right Corner
size_label = tk.Label(root, text="", bg=Background_Color, fg="white", font=("Arial", 10), anchor="e")
size_label.place(relx=1.0, rely=0.0, anchor="ne")  # Positioned in the top-right corner

# Start updating the size label
update_window_size()

# Start the application
root.mainloop()
