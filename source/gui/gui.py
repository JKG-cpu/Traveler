from ..systems import *

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

    # Game Details
    #region
    def display_game_details(self, details: dict, name_options) -> None:
        game_name = details["Name"] if details["Name"] else "New Save"
        if game_name == "New Save":
            details["Name"] = "New Save"
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

    def selecting_game(self, saves: dict):
        table = Table(
            show_header = False,
            box = box.SIMPLE,
            pad_edge = False,
            padding = (0, 1),
            expand = False
        )

        for _ in saves:
            table.add_column(justify = "center", no_wrap = True, width = 15)

        row_cells = []
        for slot, data in saves.items():
            base = data["Base Desc"]
            cell_text = f"{slot}\nName: {base['Name']}\nDiff: {base['Difficulty']}\nCash: {base['Cash']}\nFood: {base['Food']}"
            row_cells.append(cell_text)
        
        table.add_row(*row_cells)

        row = "─" * main_vt.measure(table).maximum

        main_vt.print(row)
        main_vt.print(table)
        main_vt.print(row)
    #endregion

    # Traveling Display
    def display_window(self, data: dict, commands: list, window_width: int = 70) -> str | None:
        day = data["day"]
        food = data["food"]["Amount"]
        cash = data["cash"]["Amount"]
        health = data["health"]
        weather = data["weather"]
        speed = data["speed"]
        distance = data["distance"]
    
        progress_percent = data["progress"]

        def progress_bar(percent, length = 35):
            filled = int(length * percent // 100)
            bar = "■" * filled + "-" * (length - filled)
            return f"[{bar}]"
        
        # Top
        border = "─" * window_width
        main_vt.print(border)

        # Columns
        left_col = f"DAY: {day}\nFOOD: {food}\nCASH: {cash}\nHEALTH: {health}"
        right_col = f"WEATHER: {weather}\nSPEED: {speed} M\\Day\nDISTANCE: {distance} miles\nPROGRESS: {progress_percent}%"

        left_lines = left_col.split("\n")
        right_lines = right_col.split("\n")

        # Padding
        column_width = 30
        total_width = column_width * 2
        padding = (window_width - total_width) // 2

        for l, r in zip(left_lines, right_lines):
            main_vt.print(" " * padding + f"{l:<{column_width}}{r:>{column_width}}")

        # Empty Line 
        print()

        # Progress bar
        bar = progress_bar(progress_percent)
        main_vt.print(bar.center(window_width - 9))
        main_vt.print(f"[italic]({progress_percent})% of the way[/]".center(window_width))

        # Empty line
        print()

        # Status
        status = "Traveling on..."
        main_vt.print(f"[italic]{status}[/]".center(window_width))

        # Bottom Border
        main_vt.print(border)

        # Command Zone
        main_vt.print("Commands:")
        print()
        for i, command in enumerate(commands, 1):
            if i == len(commands):
                main_vt.print(f"{command}")
            else:
                main_vt.print(f"{command} | ", end = "")
        print()
        return self.userInput(message = "Enter a command or press enter to continue", special_cases = [str.title, str.strip])

    # Input
    #region
    def userInput(self, message: str, end: str = " > ", special_cases: dict = None) -> str:
        userInput = self.main_text.inputTypewriter(msg = message, end = end)
        
        if special_cases:
            for func in special_cases:
                userInput = func(userInput)
        
        return userInput
    #endregion
