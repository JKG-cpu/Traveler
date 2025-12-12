from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

# Example save data
saves = {
    "Save 1": {"Base Desc": {"Name": "John", "Difficulty": "Hard", "Cash": "$500", "Food": "50 lbs"}},
    "Save 2": {"Base Desc": {"Name": "Mary", "Difficulty": "Easy", "Cash": "$1200", "Food": "80 lbs"}},
    "Save 3": {"Base Desc": {"Name": "Alex", "Difficulty": "Medium", "Cash": "$750", "Food": "60 lbs"}},
}

# Create table with thin borders
table = Table(
    show_header=False,
    box=box.SIMPLE,
    pad_edge=False,
    padding=(0, 1),
    expand=False
)

# Add one column per save
for _ in saves:
    table.add_column(justify="center", no_wrap=True, width=15)

# Build one row with all saves' info
row_cells = []
for slot, data in saves.items():
    base = data["Base Desc"]
    cell_text = f"{slot}\nName: {base['Name']}\nDiff: {base['Difficulty']}\nCash: {base['Cash']}\nFood: {base['Food']}"
    row_cells.append(cell_text)

# Add the single row to table
table.add_row(*row_cells)

console.print(table)
