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
        # Game Details
        difficulty = f"Difficulty: {details["Difficulty-Selection"]}"

        game_line = "+--" + ("-" * max(len(details["Name"] if details["Name"] else "New Save"), len(difficulty))) + "--+"
        full_game_line = "+--" + (("-" * (len(game_line) - 3)) + "---" + ("-" * (len(game_line) - 3))) + "--+"

        main_vt.print(game_line, end = "   ")
        main_vt.print(game_line)
        main_vt.print(details["Name"].center(len(game_line)) if details["Name"] else "New Save".center(len(game_line)), end = "   ")
        main_vt.print(difficulty.center(len(game_line)))
        main_vt.print(game_line, end = "   ")
        main_vt.print(game_line)
        print()

        section = details["Difficulty"][details["Difficulty-Selection"]]

        main_vt.print(full_game_line)
        main_vt.print("  Settings ".center(len(full_game_line)))
        main_vt.print(full_game_line)
        main_vt.print(f"   - Starting Cash: {section["Starting Cash"]}")
        main_vt.print(f"   - Starting Food: {section["Starting Food"]}")
        main_vt.print("")

        # Character Details
        character = details["Character"]

        name_text = f"Name: {character["Name"]}" if character["Name"] else f"Name: {random.choice(self.name_options.get(character["Gender"], self.name_options[random.choice(["Male", "Female"])]))}"
        age_text = f"Age: {character["Age"]}" if character["Age"] else "Age: 20"
        gender_text = f"Gender: {character["Gender"]}" if character["Gender"] else "Gender: Male"

        char_line = "+--" + (
            "-" * len(name_text) + "---" +
            "-" * len(age_text) + "---" + 
            "-" * len(gender_text)
        ) + "--+"

        main_vt.print(char_line)
        character_dis = "Character".center(len(char_line))
        main_vt.print(f"[italic]{character_dis}[/]")
        main_vt.print(char_line)
        main_vt.print(f"   {name_text}   {age_text}   {gender_text}   ")
        main_vt.print(char_line)

    def create_new_game(self) -> None:
        running = True
        details = self.game_options.copy()

        while running:
            self.display_game_details(details)
            running = False

    def load_save(self, number: str | int) -> None:
        if isinstance(number, int):
            number = str(number)

        self.current_loaded_save = self.full_data[f"Save {number}"]



    