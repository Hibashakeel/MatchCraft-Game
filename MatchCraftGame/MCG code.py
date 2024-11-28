import tkinter as tk
from tkinter import messagebox
import random
import os

# Game parameters
cards = []
card_buttons = []
selected = []
moves = 0
matches = 0
time_left = 30
game_started = False
game_won = False  # Declare the variable as False initially, before game starts
player_name = ""
rows = 3
columns = 3

# Stack to keep track of the game screens (levels, start screen, etc.)
screen_stack = []

# Create the root window
root = tk.Tk()
root.title("Match Craft Game")

# List of emojis for the horror/zombie theme (skulls, ghosts, bats, etc.)
emojis = ['🦋', '🦚', '🦜', '🐓', '🐣', '🦃', '🐧', '🦅', '🐥', '🐦', '🦉', '🦆',
          '🐔', '🦢', '🦩', '🦆', '🦦', '🐤', '🐝', '🕊']

# Function to initialize the game setup based on level
def setup_game():
    global cards, selected, moves, matches, time_left, rows, columns, game_won
    selected = []
    moves = 0
    matches = 0
    game_won = False  # Reset game_won when setting up a new game
    if level_var.get() == "Hard":
        rows = 3
        columns = 8
        time_left = 60
    elif level_var.get() == "Medium":
        rows = 3
        columns = 6
        time_left = 45
    else:  # Easy
        rows = 3
        columns = 4
        time_left = 30

    # Update card list based on grid size
    cards = []
    for emoji in emojis[:(rows * columns) // 2]:
        cards.append(emoji)
        cards.append(emoji)  # Add a pair for each emoji
    random.shuffle(cards)  # Shuffle cards

    # Create the grid based on the selected level
    create_grid()

# Function to update the score label
def update_score():
    score_label.config(text=f"Moves: {moves} | Matches: {matches} | Time: {time_left}")

# Function to flip a card
def flip(row, col):
    global selected, moves, matches, game_won  # Use the global game_won here
    if time_left <= 0 or game_won:  # No more moves after time is up or if game is won
        return
    index = row * columns + col
    if index in selected or len(selected) >= 2:
        return

    card_buttons[index].config(text=cards[index], font=("Helvetica", 20))
    selected.append(index)

    if len(selected) == 2:
        idx1, idx2 = selected
        moves += 1
        update_score()
        root.update()  # Ensure GUI updates instantly

        if cards[idx1] == cards[idx2]:
            matches += 1
            card_buttons[idx1].config(state=tk.DISABLED)  # Disable matched cards
            card_buttons[idx2].config(state=tk.DISABLED)
            selected = []  # Reset selected cards
            if matches == len(cards) // 2:
                game_won = True
                end_game(True)
        else:
            root.after(1000, lambda idx1=idx1, idx2=idx2: unflip(idx1, idx2))

# Function to unflip cards if not matched
def unflip(idx1, idx2):
    global selected
    if card_buttons[idx1]['state'] != tk.DISABLED and card_buttons[idx2]['state'] != tk.DISABLED:
        card_buttons[idx1].config(text="", font=("Helvetica", 20))
        card_buttons[idx2].config(text="", font=("Helvetica", 20))
    selected.clear()  # Reset selected cards

# Function to start the game
def start_game(event=None):
    global game_started, player_name
    player_name = name_entry.get()
    if player_name == "":
        messagebox.showinfo("Error", "Please enter your name!")
        return
    # Hide name entry and level selection widgets
    start_label.pack_forget()
    start_label1.pack_forget()
    name_entry.pack_forget()
    level_menu.pack_forget()
    # Setup and start the game
    setup_game()
    countdown()
    game_started = True
    screen_stack.append("Game")  # Push the game screen to stack

# Function to start the countdown timer and write the score in text file
def countdown():
    global time_left
    if game_won:  # Stop countdown if the game is won
        return
    if time_left > 0:
        time_left -= 1
        update_score()
        root.after(1000, countdown)
    else:
        end_game(False)

# Function to show the game over dialog with buttons
def end_game(victory):
    global moves, matches, player_name, game_won
    game_won = victory
    if victory:
        message = f"Congratulations! You won the game!\nMoves: {moves}\nMatches: {matches}"
    else:
        message = f"Time's up! You made {moves} moves and found {matches} matches."
         
        with open("scoreLO.txt", "a") as f:
            f.write(f"Player: {player_name}\n")
            f.write(f"Moves: {moves}\n")
            f.write(f"Matches: {matches}\n")
            f.write("\n")

    # Ensure file is being written to correctly
    file_path = os.path.join(os.getcwd(), "high_score.txt")  # Absolute path to the current directory
    print(f"Saving results to: {file_path}")  # Debug print to verify file path

    # Write the result to a file (append mode)
    with open(file_path, "a") as file:
        file.write(f"Player: {player_name}, Moves: {moves}, Matches: {matches}, Victory: {game_won}\n")
        file.flush()  # Ensure immediate write
        print(f"Results written to file: {file_path}")

    # Disable all buttons
    for button in card_buttons:
        button.config(state=tk.DISABLED)

    result_label.config(text=message)
    result_frame.pack(pady=20)  # Show the result frame after the game ends

# Function to reset the game state
def reset_game():
    global cards, card_buttons, selected, moves, matches, time_left
    cards.clear()
    card_buttons.clear()
    selected.clear()
    moves = 0
    matches = 0
    time_left = 30  # Reset to default or chosen value

# Replay button handler
def replay_game():
    result_frame.pack_forget()  # Hide the result frame
    reset_game()
    setup_game()
    countdown()

# Skip button handler - Show "Game Over" screen
def skip_game():
    # Hide the current game screen
    for button in card_buttons:
        button.config(state=tk.DISABLED)
    result_label.config(text="Game Over!")
    result_frame.pack(pady=20)

# Play Another Level button handler
def play_another_level():
    global screen_stack
    # Reset the game state before showing the level selection screen again
    result_frame.pack_forget()  # Hide the result frame
    reset_game()
    setup_level_selection()  # Show the level selection screen after the game ends

# Function to set up the level selection screen again
def setup_level_selection():
    global game_started
    # Show the level selection screen again (level options and start button)
    start_label.pack(pady=10)
    start_label1.pack(pady=10)
    name_entry.pack(pady=10)
    level_menu.pack(pady=10)
    game_started = False
    screen_stack.append("LevelSelection")  # Push level selection screen to stack

# Function to create the grid based on the level
def create_grid():
    global card_buttons, rows, columns
    # First, clear the existing grid if any
    for button in card_buttons:
        button.grid_forget()
    card_buttons.clear()

    # Create a new grid for the selected level
    for i in range(rows):
        for j in range(columns):
            button = tk.Button(frame, text="", width=5, height=2, font=("Helvetica", 20), bg="chocolate", fg="white", relief="raised", command=lambda row=i, col=j: flip(row, col))
            button.grid(row=i, column=j, padx=5, pady=5)
            card_buttons.append(button)

# Label to display game score
score_label = tk.Label(root, text="Time", font=("times", 16), bg="bisque", fg="sienna")
score_label.pack(pady=10)

# Label to prompt for player name
start_label1 = tk.Label(root, text="Enter your name", font=("times", 16), bg="bisque", fg="sienna")
start_label1.pack(pady=10)

# Entry for player name
name_entry = tk.Entry(root, font=("times", 16), bg="white", fg="black", insertbackground="white")
name_entry.pack(pady=10)

start_label = tk.Label(root, text="Select a level to start the game", font=("times", 16), bg="bisque", fg="sienna")
start_label.pack(pady=10)

# Dropdown menu to select difficulty level
level_var = tk.StringVar(value="Level")
level_menu = tk.OptionMenu(root, level_var, "Easy", "Medium", "Hard")
level_menu.config(bg="navajowhite", fg="black", font=("times", 16))
level_menu.pack(pady=10)

# Add a frame for game area
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Add result frame to show game over messages
result_frame = tk.Frame(root)
result_label = tk.Label(result_frame, text="", font=("times", 14), bg="peachpuff", fg="chocolate")
result_label.pack(pady=10)

# Buttons for retrying or skipping game
button_frame = tk.Frame(result_frame)
retry_button = tk.Button(button_frame, text="Retry", font=("times", 14), bg="peachpuff", fg="chocolate", command=replay_game)
retry_button.pack(side="left", padx=10)
skip_button = tk.Button(button_frame, text="Skip", font=("times", 14), bg="peachpuff", fg="chocolate", command=skip_game)
skip_button.pack(side="right", padx=10)  # Align on the right side

# Play Another Level button
play_another_button = tk.Button(button_frame, text="Play Another Level", font=("times", 14), bg="peachpuff", fg="chocolate", command=play_another_level)
play_another_button.pack(side="right", padx=10)  # Align on the right side

# Pack the button_frame into result_frame to show buttons
button_frame.pack(pady=10)

# Initially hide the result frame
result_frame.pack_forget()

# Start button (Enter key is bound to start_game)
start_button = tk.Button(root, text="Start Game", font=("times", 16), command=start_game)
start_button.pack(pady=20)

# Configure the background color
frame.configure(bg='lemonchiffon')
root.configure(bg='lemonchiffon')

# Run the game loop
root.mainloop()
