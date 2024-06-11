import tkinter as tk
from tkinter import filedialog
import os
from os.path import join, getsize
import ctypes
from ctypes import wintypes
import re
import json
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
import tempfile

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

#Turn nested dict into flat dict for displaying
def get_plot_data(data):
    returndict = {}
    for key in data.keys():
        if not re.match("^__.*__$", key):
            returndict[key] = data[key]["__totdirsize__"]
    return returndict

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

    dir_split = re.split("/|\\\\", dir_in)
    folder_name = dir_split[-1]
    dir_path = '/'.join(dir_split[:-1])
    dir_dict = {"__dirname__": folder_name, "__dirpath__": dir_path}
    totalSize = 0
    for root, dirs, files in os.walk(dir_in):
        root_short = get_short_path_name(root)
        filesizes = [getsize(join(root_short, name)) for name in files]
        dir_dict['__filesizes__'] = filesizes
        dir_dict['__filenames__'] = files
        dir_dict['__totfilesize__'] = sum(filesizes)
        totalSize = dir_dict['__totfilesize__']
        for nextdir in dirs:
            nextret = analyze_directory_recursive(join(root_short, nextdir))
            dir_dict[nextdir] = nextret[0]
            totalSize = totalSize + nextret[1]
        

        dir_dict['__totdirsize__'] = totalSize
        break
    if "__totdirsize__" not in dir_dict:
        dir_dict['__totdirsize__'] = 0
    return [dir_dict, totalSize]


def plot_directory(data_dict):
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.3)])
    fig.update_layout(title_text='Directory Size Distribution')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    fig.write_html(temp_file.name)
    webbrowser.open('file://' + temp_file.name)

def main():
    # root = tk.Tk()
    # root.withdraw()
    #analyze_directory()
    directory = filedialog.askdirectory()
    if not directory:
        return
    #print(json.dumps(analyze_directory_recursive(directory), indent=4))
    nested_data, _ = analyze_directory_recursive(directory)
    flat_data = get_plot_data(nested_data)
    plot_directory(flat_data)
    #print(analyze_directory_recursive(directory))
    # root.mainloop()

if __name__ == "__main__":
    main()