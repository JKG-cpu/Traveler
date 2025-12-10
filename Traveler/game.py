from .settings import *
from .gui import GUI

class Game:
    def __init__(self, file_path):
        self.GameLoader = GameLoader(file_path)
        self.gui = GUI()

    # Creating a game
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

    def create_new_game(self) -> tuple[bool, str] | tuple[bool, None]:
        """
        Docstring for create_new_game
        
        :returns: True if a new save is created, False if a new save is canceled
        :rtype: tuple[bool, str] | tuple[bool, None]
        """
        # Check if more than 3 saves
        if all(save["Used"] for save in self.GameLoader.data.values()):
            return False

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
                self.GameLoader.new_save(
                    details = details
                )
                running = False

            else:
                self.gui.wrong_option()