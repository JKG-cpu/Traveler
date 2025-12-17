from ..systems import *
from ..gui import *

class EventManager:
    def __init__(self, file_path: str) -> None:
        self.eventLoader = EventLoader(file_path)
        self.data = self.eventLoader.data
        self.no_event_chance = .5

        self.base_return_template = {
            "day": 0,
            "food": 0
        }

        self.gui = GUI()

    # Get Events
    def road_event(self) -> dict | None:
        road_events = self.data["road_events"] + [None]
        road_event_chances = [item["trigger_chance"] for item in self.data["road_events"]] + [self.no_event_chance]

        return random.choices(road_events, weights = road_event_chances, k = 1)[0]

    def party_event(self) -> dict | None:
        pass

    def town_event(self) -> dict | None:
        pass

    def enviroment_event(self) -> dict | None:
        pass

    def positive_event(self) -> dict | None:
        pass

    # Run Events
    def run_event(self, event: dict) -> dict:
        changes = self.base_return_template.copy()

        # Grab Event Details
        name = event["Name"]
        details = event["Description"]
        choices = event["Choices"]
        choice_amount = len(choices)
        text_color = event.get("Color", "white")
        
        while True:
            cc()
            # Display Event Details
            self.gui.display_event(
                name = name,
                text_color = text_color,
                desc = details,
                choices = choices
            )

            # Get User Input
            user_input = self.gui.userInput(
                message = "Select an option",
                special_cases = [
                    str.strip
                ]
            )

            if not user_input.isdigit():
                self.gui.wrong_option()
                continue

            user_input = int(user_input)

            if user_input <= choice_amount > 0:
                item = choices[user_input - 1]

                for effect in item["effects"]:
                    changes[effect] = changes.get(effect, 0) + item["effects"][effect]

                # Display Effects
                # Need to fix effect printing...
                main_vt.print(f"You choose: {details}")
                main_vt.print(f"Effects caused: {f" | ".join(f"{key}: {value}" for key, value in item["effects"].items())}")
                main_vt.input("Press Enter to continue. ")

                return changes
    
            else:
                self.gui.wrong_option()
