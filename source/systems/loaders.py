from .settings import *
import pprint

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

        self.empty_save = {
            "FilePath": "",
            "Base Desc": {
            "Difficulty": "",
            "Name": "",
            "Cash": "",
            "Food": ""
            },
            "Used": False
        }
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
            },

            "Inventory": [],

            "Event": "Traveling",
            "Event-types": {
                "Traveling": {
                    "day": 0,
                    "weather": "",
                    "speed": 3,
                    "distance": 0,
                    "total_dist": 0,
                    "progress": 0
                },
                "In-Town": {},
                "Event": {},
                "Paused": {}
            }
        }
        self.name_options = {
            "Male": ["James", "Michael", "William", "David", "Daniel"],
            "Female": ["Emily", "Olivia", "Sophia", "Ava", "Isabella"]
        }

    def load_save(self, number: str | int) -> None:
        file_path = self.data[f"Save {number}"]["FilePath"]
        self.current_loaded_save = (self.load_data(filepath = file_path), file_path)

    def new_save(self, details: dict) -> int | bool:
        for save in self.data:
            if not self.data[save]["Used"]:
                # Main Save
                self.data[save]["Used"] = True
                head = self.data[save]["Base Desc"]
                head["Difficulty"] = details["Difficulty-Selection"]
                head["Name"] = details["Name"]
                head["Cash"] = details["Difficulty"][details["Difficulty-Selection"]]["Starting Cash"]
                head["Food"] = details["Difficulty"][details["Difficulty-Selection"]]["Starting Food"]

                # Add Specific Items to inventory
                details["Inventory"].append({
                    "Name": "Food",
                    "Amount": details["Difficulty"][details["Difficulty-Selection"]]["Starting Food"],
                    "Details": "Yummy"
                })
                details["Inventory"].append({
                    "Name": "Cash",
                    "Amount": details["Difficulty"][details["Difficulty-Selection"]]["Starting Cash"],
                    "Details": "Oooh... Money!"
                })

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
                return save[-1]

        else:
            return False
        
    def valid_saves(self) -> bool:
        return any(self.data[save]["Used"] for save in self.data)

    def reset_save(self, number: str | int) -> None:
        sub_path = join(self.file_path.removesuffix(".json"), f"save{number}.json")
        save = self.empty_save.copy()

        save["FilePath"] = sub_path

        self.data[f"Save {number}"] = save
        self.begin_process("Save", self.data)
        self.begin_process("Save", data = {}, file_path = sub_path)

class PlayerLoader(DataLoader):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)

class EventLoader(DataLoader):
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        
        # Event Types
        # self.road_events = self.data["road_events"]
        # self.party_events = self.data["party_events"]
        # self.town_events = self.data["town_events"]
        # self.enviroment_events = self.data["enviroment_events"]
        # self.positive_events = self.data["positive_events"]