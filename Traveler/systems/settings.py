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
    
    def begin_process(self, type: str, data: dict = None, instant: bool = False, file_path: str | None = None) -> None:
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
            threading.Thread(target = self.load_data, args = (file_path,)).start()

        elif type == "Save":
            if data == None:
                raise TypeError(f"\nInvalid Data in {self.__class__.__name__}.{self.__class__.begin_process.__name__}(); data = {data}")
            threading.Thread(target = self.save_data, args = (data, file_path,)).start()

        else:
            raise TypeError(f"\nInvalid Type in {self.__class__.__name__}.{self.__class__.begin_process.__name__}(); Type = {type}")

    def load_data(self, filepath: str | None = None) -> None | dict:
        if filepath:
            try:
                with open(filepath, "r") as f:
                    return json.load(f)

            except Exception as e:
                error_vt.print(f"Error Loading Data: {e}")
                input()
            
            return

        try:
            with open(self.file_path, "r") as f:
                self.data = json.load(f)

        except Exception as e:
            error_vt.print(f"Error Loading Data: {e}")
            self.data = {}
            input()

    def save_data(self, data: dict | list, filepath: str | None = None):
        if filepath:
            try:
                with open(filepath, "w") as f:
                    json.dump(data, f, indent = 2)
            
            except Exception as e:
                error_vt.print(f"Error Saving Data: {e}")
                input()

            return

        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent = 2)
        
        except Exception as e:
            error_vt.print(f"Error Saving Data: {e}")
            input()

class GameLoader(DataLoader):
    def __init__(self, file_path: str):
        super().__init__(file_path)

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

    def load_save(self, number: str | int) -> None:
        file_path = self.data[f"Save {number}"]["FilePath"]
        self.current_loaded_save = self.load_data(filepath = file_path)

    def new_save(self, details: dict) -> None | bool:
        for save in self.data:
            if not self.data[save]["Used"]:
                # Main Save
                self.data[save]["Used"] = True
                head = self.data[save]["Base Desc"]
                head["Difficulty"] = details["Difficulty-Selection"]
                head["Name"] = details["Name"]
                head["Cash"] = details["Difficulty"][details["Difficulty-Selection"]]["Starting Cash"]
                head["Food"] = details["Difficulty"][details["Difficulty-Selection"]]["Starting Food"]


                # Remove Difficulty Settings from Details
                details.pop("Difficulty")
                file_path = self.data[save]["FilePath"]
                self.begin_process(
                    type = "Save",
                    data = details,
                    file_path = file_path
                )
                self.begin_process(
                    type = "Save",
                    data = self.data
                )
                break

        else:
            return False
        
class PlayerLoader(DataLoader):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        