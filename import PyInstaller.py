import PyInstaller.__main__
import os
from pathlib import Path

# Get the path to the user's home directory
home_directory = Path.home()

# Construct the path to the Downloads directory
downloads_directory = home_directory / "Downloads"

# Change the current working directory to the Downloads directory
os.chdir(downloads_directory)

print(f"Successfully navigated to: {os.getcwd()}")

# Run the script to make Python file into an EXE file
PyInstaller.__main__.run([
'"Card Game.py"',
'--onefile',
'--windowed',
'--icon=icon2.ico',
'--add-data "images;images"',
'--add-data "card_game_saves.json;."',
'--add-data "card_game_leaderboard.json;."',
])
