from ..systems import *
from ..gui import *
from .event import EventManager

class TravelManager:
    def __init__(self) -> None:
        self.gui = GUI()
        self.travel_ranges = [50, 75, 100, 125]
        self.commands = [
            "Speed", "Quit"
        ]

        self.events = EventManager(join("source", "data", "events.json"))

    # Make / Change Values
    def new_travel(self) -> int:
        return int(random.choice(self.travel_ranges))

    def change_speed(self) -> int:
        while True:
            print()
            user_input = self.gui.userInput(
                message = "Select a speed to move (1 - 5)",
                special_cases = [
                    str.title, str.strip
                ]
            )

            if user_input in "12345":
                return int(user_input)

            else:
                self.gui.wrong_option()

    # Run
    def run(self, data: dict, new_travel: bool = False) -> None | str:
        # Check Data
        traveling = data["Event-types"]["Traveling"]
        inventory = data["Inventory"]

        cash = [item for item in inventory if item["Name"] == "Cash"][0]
        food = [item for item in inventory if item["Name"] == "Food"][0]
        
        if new_travel:
            traveling["distance"] = self.new_travel()
            traveling["total_dist"] = traveling["distance"]
            traveling["progress"] = 0

        fixed_data = {
            "day": traveling["day"],
            "food": food,
            "cash": cash,
            "health": "Good",
            "weather": traveling["weather"],
            "speed": traveling["speed"],
            "distance": traveling["distance"],
            "total_dist": traveling["total_dist"],
            "progress": traveling["progress"]
        }

        # Display Data
        user_input = self.gui.display_window(fixed_data, self.commands)

        # Check input
        if user_input.startswith("S"):
            traveling["speed"] = self.change_speed()
            return None
        
        if user_input.startswith("Q"):
            return "Quit"

        traveling["distance"] -= traveling["speed"]
        traveling["progress"] = int(((traveling["total_dist"] - traveling["distance"]) / traveling["total_dist"]) * 100)

        traveling["day"] += 1

        if traveling["distance"] <= 0:
            traveling["distance"] = 0
            traveling["progress"] = 100
            return "In-Town"

        print(self.events.road_event())
        input()

        return None