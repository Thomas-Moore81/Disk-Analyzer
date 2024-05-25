import tkinter as tk
from tkinter import filedialog
import os
from os.path import join, getsize
import ctypes
from ctypes import wintypes
_GetShortPathNameW = ctypes.windll.kernel32.GetShortPathNameW
_GetShortPathNameW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
_GetShortPathNameW.restype = wintypes.DWORD


def get_short_path_name(long_name):
    #Gets the short path name of a given long path.
    #http://stackoverflow.com/a/23598461/200291
    output_buf_size = 0
    while True:
        output_buf = ctypes.create_unicode_buffer(output_buf_size)
        needed = _GetShortPathNameW(long_name, output_buf, output_buf_size)
        if output_buf_size >= needed:
            return output_buf.value
        else:
            output_buf_size = needed


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
        root = get_short_path_name(root)
        dirBytes = sum(getsize(join(root, name)) for name in files)
        dirsizes[root] = dirBytes
        totalBytes += dirBytes
        print(f"{root} consumes {dirBytes} bytes in {len(files)} its files")

    totalGB = totalBytes / (1024**3)
    print("Directory sizes:", dirsizes)
    print("File sizes:", filesizes)
    print(f"Total gigabytes consumed: {round(totalGB, 2)}")
    
def main():
    # root = tk.Tk()
    # root.withdraw()
    analyze_directory()
    # root.mainloop()

if __name__ == "__main__":
    main()