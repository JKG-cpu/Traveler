from Traveler import *

# Main Menu
class Main:
    def __init__(self) -> None:
        self.running = True
        self.menu_options = ["New Game", "Resume Game", "Settings", "Quit"]

        self.gui = GUI()
        self.game = Game(join(HEAD_DATA_FOLDER, "saves.json"))

    # New Game
    def new_game(self) -> bool:
        """
        :return: Returns False for quit and True for main menu
        :rtype: bool
        """
        return_to_main_menu = True

        return return_to_main_menu

    # Resume Game
    def resume_game(self) -> bool:
        """
        :return: Returns False for quit and True for main menu
        :rtype: bool
        """
        return_to_main_menu = True

        return return_to_main_menu

    # Settings
    def settings(self) -> None:
        """
        ## Docstring for settings

        ---
        
        ### Possible Changes
            * Text Colors
        """
        pass

    # Quit
    def quit(self):
        self.running = False
        cc()

    def run(self) -> None:
        while self.running:
            cc() # Clear Screen
            
            self.gui.display_options(self.menu_options)

            userInput = self.gui.userInput(
                message = "Enter an option",
                special_cases = [
                    str.title, str.strip
                ]
            )

            if userInput.startswith("Q"):
                self.quit()
            
            elif userInput.startswith("N"):
                main_menu = self.new_game()
                if not main_menu:
                    self.quit()

            elif userInput.startswith("R"):
                main_menu = self.resume_game()
                if not main_menu:
                    self.quit()

            elif userInput.startswith("S"):
                self.settings()
            
            else:
                self.gui.wrong_option()

    def test(self) -> None:
        self.game.play_game(1)

if __name__ == "__main__":
    main = Main()
    main.test()