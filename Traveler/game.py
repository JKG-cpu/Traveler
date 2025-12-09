from .settings import *
from .gui import GUI

class Game:
    def __init__(self, file_path):
        self.GameLoader = GameLoader(file_path)
        self.gui = GUI()

    def create_new_game(self) -> bool:
        """
        Docstring for create_new_game
        
        :returns: True if a new save is created, False if a new save is canceled
        :rtype: bool
        """
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
            "Character": [

            ]
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
                pass

            elif user_input.startswith("N"):
                pass

            elif user_input.startswith("Ch"):
                pass

            elif user_input.startswith("Cr"):
                pass

            else:
                self.gui.wrong_option()