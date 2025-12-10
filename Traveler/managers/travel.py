from ..systems import *
from ..gui import *

class TravelManager:
    def __init__(self) -> None:
        self.gui = GUI()

    def run(self, data: dict) -> None | str:
        # Check Data
        

        # Display Data
        user_input = self.gui.display_window(data)

        # Check input
        main_vt.print(user_input)

        return None