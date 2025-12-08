from Traveler import *

# Main Menu
class Main:
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    main = Main()
    data = DataLoader(join(HEAD_DATA_FOLDER, "test.json"))
    print(data.data)