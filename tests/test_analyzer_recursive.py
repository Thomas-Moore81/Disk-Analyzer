import tkinter as tk
from tkinter import filedialog
import os
from os.path import join, getsize
import ctypes
from ctypes import wintypes
import re
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


# def analyze_directory():
#     #tkinter dialog box for directory selection
#     directory = filedialog.askdirectory()
#     #user canceled selection
#     if not directory:
#         return
    
#     dirsizes = {}
#     filesizes = {}
#     totalBytes = 0

#     for root, dirs, files in os.walk(directory, topdown=False):
#         root_short = get_short_path_name(root)
#         dirBytes = sum(getsize(join(root_short, name)) for name in files)
#         dirsizes[root_short] = dirBytes
#         totalBytes += dirBytes
#         dir_split = re.split("/|\\\\", root)
#         folder_name = dir_split[-1]
#         dir_path = '/'.join(dir_split[:-1])
#         print(f"DIRNAME: {folder_name}\nDIRPATH: {dir_path}")

#     totalGB = totalBytes / (1024**3)
#     print("Directory sizes:", dirsizes)
#     print("File sizes:", filesizes)
#     print(f"Total gigabytes consumed: {round(totalGB, 2)}")

def analyze_directory_recursive(dir_in):

    dirsizes = {}
    filesizes = {}

    dir_split = re.split("/|\\\\", dir_in)
    folder_name = dir_split[-1]
    dir_path = '/'.join(dir_split[:-1])
    dir_dict = {"__dirname__": folder_name, "__dirpath__": dir_path}
    totalBytes = 0
    for root, dirs, files in os.walk(dir_in):
        root_short = get_short_path_name(root)
        dir_dict['__filesizes__'] = sum(getsize(join(root_short, name)) for name in files)
        for nextdir in dirs:
            dir_dict[nextdir] = analyze_directory_recursive(join(root_short, nextdir))

        break
    return dir_dict
def main():
    # root = tk.Tk()
    # root.withdraw()
    #analyze_directory()
    directory = filedialog.askdirectory()
    if not directory:
        return
    print(analyze_directory_recursive(directory))
    # root.mainloop()

if __name__ == "__main__":
    main()