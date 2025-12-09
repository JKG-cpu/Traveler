from .settings import *

class GUI:
    def __init__(self) -> None:
        # Typewriters
        self.main_text = vt(bold = True, sleep = .03)
        
        # Quick Printers
        self.quick_text = Console()
        self.quick_text.style = "bold white"

    # Display
    def display_options(self, options: list[str]) -> None:
        worded = []
        for i, option in enumerate(options, 1):
            if i == len(options):
                worded.append(f"{option} ")
            else:
                worded.append(f"{option} | ")
        
        self.quick_text.print("".join(worded))

    def wrong_option(self) -> None:
        self.main_text.typewriter("That is not a valid option...")
        self.main_text.inputTypewriter("Press Enter to Continue.", end = "")

    # Input
    def userInput(self, message: str, special_cases: dict = None) -> str:
        userInput = self.main_text.inputTypewriter(msg = message)
        
        if special_cases:
            for func in special_cases:
                userInput = func(userInput)
        
        return userInput
