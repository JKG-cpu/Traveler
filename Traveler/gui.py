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

    def display_game_details(self, details: dict, name_options) -> None:
        game_name = details["Name"] if details["Name"] else "New Save"
        difficulty = f"Difficulty: {details['Difficulty-Selection']}"

        section = details["Difficulty"][details["Difficulty-Selection"]]
        settings = [
            f"Starting Cash: {section['Starting Cash']}",
            f"Starting Food: {section['Starting Food']}"
        ]

        character = details["Character"]
        gender_selected = character["Gender"] if character["Gender"] else random.choice(["Male", "Female"])
        gender_text = f"Gender: {gender_selected}"
        name_selected = character["Name"] if character["Name"] else random.choice(name_options.get(gender_selected))
        name_text = f"Name: {name_selected}"
        age_selected = character["Age"] if character["Age"] else str(random.randint(18, 30))
        age_text = f"Age: {age_selected}"
        
        character["Name"] = name_selected
        character["Age"] = age_selected
        character["Gender"] = gender_selected

        char_line_content = f"{name_text}  {age_text}  {gender_text}"

        all_lines = [game_name, difficulty] + settings + [char_line_content, "Character", "Settings"]
        box_width = max(len(line) for line in all_lines) + 4
        border = f"+{'-' * box_width}+"

        main_vt.print("Game Settings".center(box_width + 2))
        main_vt.print(border)
        main_vt.print(f"| {game_name.center(box_width - 2)} |")
        main_vt.print(f"| {difficulty.center(box_width - 2)} |")
        main_vt.print(border)
        print()

        main_vt.print(border)
        main_vt.print(f"  Settings ".center(box_width + 2))
        main_vt.print(border)
        for s in settings:
            main_vt.print(f"| {s.ljust(box_width - 2)} |")
        main_vt.print(border)
        print()

        main_vt.print(border)
        main_vt.print(f"[italic]{' Character'.center(box_width)}[/]")
        main_vt.print(border)
        main_vt.print(f"| {char_line_content.center(box_width - 2)} |")
        main_vt.print(border)
        print()

    def display_character_details(self, details: dict):
        name = f"Name: {details["Name"]}"
        age = f"Age: {details["Age"]}"
        gender = f"Gender: {details["Gender"]}"

        longest_line = f"+{"-" * (len(name) + len(age) + len(gender) + 8)}+"

        main_vt.print(longest_line)
        main_vt.print(f" {name} | {age} | {gender} ".center(len(longest_line)))
        main_vt.print(longest_line)

    # Input
    def userInput(self, message: str, special_cases: dict = None) -> str:
        userInput = self.main_text.inputTypewriter(msg = message)
        
        if special_cases:
            for func in special_cases:
                userInput = func(userInput)
        
        return userInput
