from ..systems import *
from ..gui import *

class TravelManager:
    def __init__(self) -> None:
        self.gui = GUI()
        self.travel_ranges = [50, 75, 100, 125]

    # Make Values
    def new_travel(self) -> int:
        return random.choice(self.travel_ranges)

    # Run
    def run(self, data: dict, new_travel: bool = False) -> None | str:
        # Check Data
        traveling = data["Event-types"]["Traveling"]
        inventory = data["Inventory"]

        cash = [item for item in inventory if item["Name"] == "Cash"][0]
        food = [item for item in inventory if item["Name"] == "Food"][0]
        
        if new_travel:
            traveling["distance"] = self.new_travel()

        fixed_data = {
            "day": traveling["day"],
            "food": food,
            "cash": cash,
            "health": "Good",
            "weather": traveling["weather"],
            "speed": traveling["speed"],
            "distance": traveling["distance"],
            "progress": traveling["progress"]
        }

        # Display Data
        user_input = self.gui.display_window(fixed_data)

        # Check input
        main_vt.print(user_input)

        return None