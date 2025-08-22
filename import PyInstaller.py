import PyInstaller.__main__
import os
from pathlib import Path

# Change the current working directory to the Downloads directory
os.chdir(r"C:\Users\s977168\Downloads")

print(f"Successfully navigated to: {os.getcwd()}")

# Run the script to make Python file into an EXE file
PyInstaller.__main__.run([
'"Card Game.py"',
'--add-data "images:images"',
'--add-data "card_game_saves.json:."',
'--add-data "card_game_leaderboard.json:."',
'--onefile',
'--windowed',
'--icon=icon2.ico'
])
