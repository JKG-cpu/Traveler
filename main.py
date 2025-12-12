from Traveler import *

# Main Menu
class Main:
    def __init__(self) -> None:
        self.running = True
        self.menu_options = ["New Game", "Resume Game", "Settings", "Quit"]

        self.gui = GUI()
        self.game = Game(join(HEAD_DATA_FOLDER, "saves.json"))

    # New Game
    def new_game(self) -> tuple[bool, int] | tuple[bool, None]:
        return_to_main_menu = True

        return_value = self.game.create_new_game()

        return return_value

    # Resume Game
    def resume_game(self, save_number: int | None = None) -> bool:
        """
        :return: Returns False for quit and True for main menu
        :rtype: bool
        """
        cc()
        return_to_main_menu = True

        if save_number is None:
            # Select Save
            while True:
                # Display Saves
                self.gui.selecting_game(self.game.GameLoader.data)
                break

                # Select Save
                self.gui.userInput()

            save_number = 1

        self.game.play_game(save_number)

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
                return_value = self.new_game()
                if return_value[1] is None:
                    main_tp.typewriter("All saves used!")
                    self.gui.userInput("Press Enter to continue.", end = " ")
                    continue
                self.resume_game(return_value[1])

            elif userInput.startswith("R"):
                main_menu = self.resume_game()
                if not main_menu:
                    self.quit()

            elif userInput.startswith("S"):
                self.settings()
            
            else:
                self.gui.wrong_option()

if __name__ == "__main__":
    main = Main()
    main.run()