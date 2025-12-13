from .systems import *
from .gui import GUI
from .models import Player
from .managers import *

class Game:
    def __init__(self, file_path):
        self.GameLoader = GameLoader(file_path)
        self.gui = GUI()
        self.player = Player()

        # Event Managers
        self.travelManager = TravelManager()

    # Creating a game
    #region
    def difficulty(self, options) -> str:
        while True:
            print()
            self.gui.display_options(options)
            print()
            user_input = self.gui.userInput(
                message = "Select an option",
                special_cases = [
                    str.title,
                    str.strip
                ]
            )
            
            if user_input.startswith("E"):
                return "Easy"

            elif user_input.startswith("M"):
                return "Medium"

            elif user_input.startswith("H"):
                return "Hard"
            
            else:
                self.gui.wrong_option()
    
    def character(self, details, options) -> None:
        while True:
            cc()

            self.gui.display_character_details(details["Character"])

            print()
            self.gui.display_options(options + ["Back"])
            print()

            user_input = self.gui.userInput(
                message = "Select an option to change",
                special_cases = [
                    str.title,
                    str.strip
                ]
            )
            
            if user_input.startswith("B"):
                break

            elif user_input.startswith("N"):
                while True:
                    print()
                    main_vt.print(" | ".join(self.GameLoader.name_options[details["Character"]["Gender"]]))
                    print()
                    new_name = self.gui.userInput(
                        message = "Enter in a name for your character",
                        special_cases = [
                            str.title, 
                            str.strip
                        ]
                    )

                    if new_name in self.GameLoader.name_options[details["Character"]["Gender"]]:
                        details["Character"]["Name"] = new_name
                        break

                    else:
                        self.gui.wrong_option()

            elif user_input.startswith("A"):
                while True:
                    print()
                    new_age = self.gui.userInput(
                        message = "What age would you like your character to be",
                        special_cases = [
                            str.strip
                        ]
                    )
                    if new_age.isdigit():
                        details["Character"]["Age"] = new_age
                        break

                    else:
                        main_vt.print("You must type in a number...")

            elif user_input.startswith("G"):
                while True:
                    print()
                    user_input = self.gui.userInput(
                        message = "Select a gender for your character",
                        special_cases = [
                            str.strip,
                            str.title
                        ]
                    )

                    if user_input == "Male":
                        details["Character"]["Name"] = random.choice(self.GameLoader.name_options["Male"])
                        details["Character"]["Gender"] = "Male"
                        break

                    elif user_input == "Female":
                        details["Character"]["Name"] = random.choice(self.GameLoader.name_options["Female"])
                        details["Character"]["Gender"] = "Female"
                        break

                    else:
                        main_vt.print("That is not a gender... Enter male or female.")

            else:
                self.gui.wrong_option()

    def create_new_game(self) -> tuple[bool, int] | tuple[bool, None]:
        """
        Docstring for create_new_game
        
        :returns: True if a new save is created, False if a new save is canceled
        :rtype: tuple[bool, str] | tuple[bool, None]
        """
        # Check if more than 3 saves
        if all(save["Used"] for save in self.GameLoader.data.values()):
            return (False, None)

        def change_value(key, value):
            details[key] = value

        running = True
        details = self.GameLoader.game_options.copy()

        options = [
            "Difficulty",
            "Name",
            "Character",
            "Create World",
            "Cancel"
        ]

        sub_options = {
            "Difficulty": ["Easy", "Medium", "Hard"],
            "Name": "Input",
            "Character": {
                "Name": "", 
                "Age": "", 
                "Gender": ["Male", "Female"]
            }
        }

        while running:
            cc()
            self.gui.display_game_details(details, self.GameLoader.name_options)

            self.gui.display_options(options)

            user_input = self.gui.userInput(
                message = "Enter in an option",
                special_cases = [
                    str.title,
                    str.strip
                ]
            )

            if user_input.startswith("Ca"):
                running = False
                return (False, None)
            
            elif user_input.startswith("D"):
                change_value(
                    key = "Difficulty-Selection", 
                    value = self.difficulty(sub_options["Difficulty"])
                )

            elif user_input.startswith("N"):
                print()
                change_value(
                    key = "Name", 
                    value = self.gui.userInput(
                        message = "Enter in a name for your save", 
                        special_cases = [str.strip]
                    )
                )

            elif user_input.startswith("Ch"):
                self.character(
                    details = details,
                    options = list(sub_options["Character"].keys())
                )

            elif user_input.startswith("Cr"):
                save_number = self.GameLoader.new_save(
                    details = details
                )
                running = False
                return (True, save_number)

            else:
                self.gui.wrong_option()
    #endregion

    # Run Game
    def play_game(self, save_number: int) -> None:
        running = True
        self.GameLoader.load_save(save_number)
        loaded_save = self.GameLoader.current_loaded_save

        # Events
        TRAVELING = False
        IN_TOWN = False
        EVENT = False
        PAUSED = False

        # Event Specific Variables
        NEW_TRAVEL = False

        # Check event from last save
        match loaded_save["Event"]:
            case "Traveling":
                TRAVELING = True
                if loaded_save["Event-types"]["Traveling"]["distance"] == 0:
                    NEW_TRAVEL = True

            case "In-Town":
                IN_TOWN = True

            case "Event":
                EVENT = True
            
            case PAUSED:
                PAUSED = True

        while running:
            if TRAVELING:
                return_value = self.travelManager.run(loaded_save, NEW_TRAVEL)
                NEW_TRAVEL = False

                if return_value == "In-Town":
                    TRAVELING = False
                    IN_TOWN = True
                    continue

                if return_value == "Quit":
                    TRAVELING = False
                    PAUSED = True
                    continue

            elif IN_TOWN:
                pass

            elif EVENT:
                pass

            elif PAUSED:
                running = False

