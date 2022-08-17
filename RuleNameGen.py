import tkinter as tk
from tkinter import filedialog

from src.ruleset import Ruleset

root = tk.Tk()
root.withdraw()


# Select ruleset
ruleset_path = filedialog.askopenfilename(
    title="Please select the ruleset.",
    filetypes=[("Ruleset files", "json")],
    initialdir=".",
)
ruleset = Ruleset.from_json(ruleset_path)

# Generate names
batch_size = int(input("Enter number of names to generate: "))
if batch_size < 1:
    batch_size = 1
generate = True
while generate:
    print("")
    for _ in range(0, batch_size):
        print(ruleset.get_name())
    generate = input(f"\nGenerate {batch_size} more names (Y/n)? ") != "n"
