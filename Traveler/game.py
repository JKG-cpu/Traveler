from .settings import *
from .gui import GUI

class Game:
    def __init__(self, file_path):
        self.GameLoader = GameLoader(file_path)
        self.gui = GUI()

    # Creating a game
    def create_new_game(self) -> tuple[bool, str] | tuple[bool, None]:
        """
        Docstring for create_new_game
        
        :returns: True if a new save is created, False if a new save is canceled
        :rtype: tuple[bool, str] | tuple[bool, None]
        """
        # Check if more than 3 saves
        if all(save["Used"] for save in self.GameLoader.full_data.values()):
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
            self.GameLoader.display_game_details(details)

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
                while True:
                    print()
                    self.gui.display_options(sub_options["Difficulty"])
                    print()
                    user_input = self.gui.userInput(
                        message = "Select an option",
                        special_cases = [
                            str.title,
                            str.strip
                        ]
                    )

                    if user_input.startswith("E"):
                        change_value("Difficulty-Selection", "Easy")
                        break

                    elif user_input.startswith("M"):
                        change_value("Difficulty-Selection", "Medium")
                        break

                    elif user_input.startswith("H"):
                        change_value("Difficulty-Selection", "Hard")
                        break
                    
                    else:
                        self.gui.wrong_option()

            elif user_input.startswith("N"):
                print()
                save_name = self.gui.userInput(
                    message = "Enter in a name for your save",
                    special_cases = [
                        str.strip
                    ]
                )
                change_value("Name", save_name)

            elif user_input.startswith("Ch"):
                pass

            elif user_input.startswith("Cr"):
                pass

            else:
                self.gui.wrong_option()