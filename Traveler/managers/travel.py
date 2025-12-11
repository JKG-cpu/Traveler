from ..systems import *
from ..gui import *

class TravelManager:
    def __init__(self) -> None:
        self.gui = GUI()

    def run(self, data: dict) -> None | str:
        # Check Data
        traveling = data["Event-types"]["Traveling"]
        inventory = data["Inventory"]

        cash = [item for item in inventory if item["Name"] == "Cash"][0]
        food = [item for item in inventory if item["Name"] == "Food"][0]

        fixed_data = {
            "day": traveling["day"],
            "food": food,
            "cash": cash,
            "health": "Good",
            "weather": traveling["weather"],
            "speed": traveling["speed"],
            "distance": traveling["distance"] if traveling["distance"] else random.choice([50, 75, 100, 125]),
            "progress": traveling["progress"]
        }

        # Display Data
        user_input = self.gui.display_window(fixed_data)

        # Check input
        main_vt.print(user_input)

        return None