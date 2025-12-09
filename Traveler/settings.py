import json
import threading
import random

from VividText import VividText as vt
from rich.console import Console
from os.path import join
from os import system, name

# Variables
error_vt = Console()
error_vt.style = "bold red"

main_vt = Console()
main_vt.style = "bold white"

# File Paths
HEAD_DATA_FOLDER = join("Traveler", "data")

# Functions
def cc():
    system("cls" if name == "nt" else "clear")

# Classes
class DataLoader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.data = None
        self.begin_process("Load", instant = True)
    
    def begin_process(self, type: str, data: dict = None, instant: bool = False) -> None:
        """
        Docstring for begin_process
        
        :param type: Type of process (Load or Save)
        :type type: str
        :param data: Data to save
        :type data: dict
        """
        if type == "Load":
            if instant: 
                self.load_data()
                return
            threading.Thread(target = self.load_data).start()

        elif type == "Save":
            if data == None:
                raise TypeError(f"\nInvalid Data in {self.__class__.__name__}.{self.__class__.begin_process.__name__}(); data = {data}")
            threading.Thread(target = self.save_data, args = (data,)).start()

        else:
            raise TypeError(f"\nInvalid Type in {self.__class__.__name__}.{self.__class__.begin_process.__name__}(); Type = {type}")

    def load_data(self):
        try:
            with open(self.file_path, "r") as f:
                self.data = json.load(f)

        except Exception as e:
            error_vt.print(f"Error Loading Data: {e}")
            self.data = {}

    def save_data(self, data: dict | list):
        try:
            with open(self.file_path, "w") as f:
                json.dump(f, data)
        
        except Exception as e:
            error_vt.print(f"Error Saving Data: {e}")

class GameLoader(DataLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path)

        self.full_data = self.data
        self.current_loaded_save = None

        self.game_options = {
            "Difficulty": {
                "Easy": {
                    "Starting Cash": "$1000",
                    "Starting Food": "75 lbs"
                },
                "Medium": {
                    "Starting Cash": "$500",
                    "Starting Food": "50 lbs"
                },
                "Hard": {
                    "Starting Cash": "$250",
                    "Starting Food": "25 lbs"
                }
            },
            "Difficulty-Selection": "Easy",
            "Name": None,
            "Character": {
                "Name": None,
                "Age": None,
                "Gender": None
            }
        }
        self.name_options = {
            "Male": ["James", "Michael", "William", "David", "Daniel"],
            "Female": ["Emily", "Olivia", "Sophia", "Ava", "Isabella"]
        }

    def display_game_details(self, details: dict):
        # --- Prepare game info ---
        game_name = details["Name"] if details["Name"] else "New Save"
        difficulty = f"Difficulty: {details['Difficulty-Selection']}"

        # Difficulty-specific settings
        section = details["Difficulty"][details["Difficulty-Selection"]]
        settings = [
            f"Starting Cash: {section['Starting Cash']}",
            f"Starting Food: {section['Starting Food']}"
        ]

        # Character details
        character = details["Character"]
        name_text = f"Name: {character['Name']}" if character['Name'] else f"Name: {random.choice(self.name_options.get(character['Gender'], self.name_options[random.choice(['Male', 'Female'])]))}"
        age_text = f"Age: {character['Age']}" if character['Age'] else "Age: 20"
        gender_text = f"Gender: {character['Gender']}" if character['Gender'] else "Gender: Male"
        char_line_content = f"{name_text}  {age_text}  {gender_text}"

        # --- Calculate unified width ---
        all_lines = [game_name, difficulty] + settings + [char_line_content, "Character", "Settings"]
        box_width = max(len(line) for line in all_lines) + 4  # padding
        border = f"+{'-' * box_width}+"

        # --- Print Game Info ---
        main_vt.print("Game Settings".center(box_width + 2))
        main_vt.print(border)
        main_vt.print(f"| {game_name.center(box_width - 2)} |")
        main_vt.print(f"| {difficulty.center(box_width - 2)} |")
        main_vt.print(border)
        print()

        # --- Print Settings ---
        main_vt.print(border)
        main_vt.print(f"  Settings ".center(box_width + 2))
        main_vt.print(border)
        for s in settings:
            main_vt.print(f"| {s.ljust(box_width - 2)} |")
        main_vt.print(border)
        print()

        # --- Print Character Info ---
        main_vt.print(border)
        main_vt.print(f"[italic]{' Character'.center(box_width)}[/]")
        main_vt.print(border)
        main_vt.print(f"| {char_line_content.center(box_width - 2)} |")
        main_vt.print(border)
        print()

    def load_save(self, number: str | int) -> None:
        if isinstance(number, int):
            number = str(number)

        self.current_loaded_save = self.full_data[f"Save {number}"]
