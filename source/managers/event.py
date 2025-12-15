from ..systems import *

class EventManager:
    def __init__(self, file_path: str) -> None:
        self.eventLoader = EventLoader(file_path)
        self.data = self.eventLoader.data
        self.no_event_chance = .5

    # Get Events
    def road_event(self) -> dict | None:
        road_events = self.data["road_events"] + [None]
        road_event_chances = [item["trigger_chance"] for item in self.data["road_events"]] + [self.no_event_chance]

        return random.choices(road_events, weights = road_event_chances, k = 1)

    def party_event(self) -> dict | None:
        pass

    def town_event(self) -> dict | None:
        pass

    def enviroment_event(self) -> dict | None:
        pass

    def positive_event(self) -> dict | None:
        pass
