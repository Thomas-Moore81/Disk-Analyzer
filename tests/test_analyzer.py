import tkinter as tk
from tkinter import filedialog
import os
from os.path import join, getsize

def analyze_directory():
    #tkinter dialog box for directory selection
    directory = filedialog.askdirectory()
    #user canceled selection
    if not directory:
        return
    
    dirsizes = {}
    filesizes = {}
    totalBytes = 0

    for root, dirs, files in os.walk(directory, topdown=False):
        dirBytes = sum(getsize(join(root, name)) for name in files)
        dirsizes[root] = dirBytes
        totalBytes += dirBytes
        print(f"{root} consumes {dirBytes} bytes in {len(files)} its files")

    totalGB = totalBytes / (1024**3)
    print(f"Total gigabytes consumed: {round(totalGB, 2)}")
    print("Directory sizes:", dirsizes)
    print("File sizes:", filesizes)

def main():
    root = tk.Tk()
    root.withdraw()
    analyze_directory()
    root.mainloop()

if __name__ == "__main__":
    main()