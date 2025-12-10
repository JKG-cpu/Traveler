import json
import threading
import random

from VividText import VividText as vt
from rich.console import Console
from os.path import join
from os import system, name

# Variables
error_vt = Console()
error_vt.style = "bold red"

main_vt = Console()
main_vt.style = "bold white"

# File Paths
HEAD_DATA_FOLDER = join("Traveler", "data")

# Functions
def cc():
    system("cls" if name == "nt" else "clear")

# Classes
