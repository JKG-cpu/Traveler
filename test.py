# test.py
SCREEN_WIDTH = 70  # total width of the screen

# Example data
day = 12
food = 48
cash = 325
health = "Good"
weather = "Mild"
speed = "Steady"
distance = 142
progress_percent = 23  # 0-100

# Function to generate progress bar
def progress_bar(percent, length=35):
    filled = int(length * percent // 100)
    bar = "■" * filled + "-" * (length - filled)
    return f"[{bar}]"

# Top border
border = "─" * SCREEN_WIDTH
print(border)

# Columns
left_col = f"DAY: {day}\nFOOD: {food} lbs\nCASH: ${cash}\nHEALTH: {health}"
right_col = f"WEATHER: {weather}\nSPEED: {speed}\nDISTANCE: {distance} miles\nPROGRESS: {progress_percent}%"

left_lines = left_col.split("\n")
right_lines = right_col.split("\n")

# Calculate padding to center the whole block
column_width = 30
total_width = column_width * 2
padding = (SCREEN_WIDTH - total_width) // 2

for l, r in zip(left_lines, right_lines):
    print(" " * padding + f"{l:<{column_width}}{r:>{column_width}}")

# Empty line
print()

# Progress bar
bar = progress_bar(progress_percent)
print(bar.center(SCREEN_WIDTH))
print(f"({progress_percent}% of the way)".center(SCREEN_WIDTH))

# Empty line
print()

# Status messages
status_msg = "Wagon is traveling..."
print(status_msg.center(SCREEN_WIDTH))

# Bottom border
print(border)

# Command Zone
input("Enter command or press enter to continue. ")