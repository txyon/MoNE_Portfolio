### Dependencies
import csv
import tkinter
import subprocess

from tkinter import filedialog

tkinter.Tk().withdraw()
fp = filedialog.askopenfilename()
fp = fp.replace('/', '\\')                                                      # Replace file path delimiters 

### Convert .raw to .es
es = fp + '.es'                                                                 # Add .es to file name in path
cmd = ("./evt3_to_es " + fp + " " + es)                                         # Command variable for powershell terminal using Command line tools - https://github.com/neuromorphic-paris/command_line_tools)
subprocess.call('G:\\PG\\command_line_tools\\build\\release' + cmd, shell=True) # Run command

### Convert .es to .csv 
csv = fp + '.csv'                                                               # Add .csv to file name in path
cmd = ("./es_to_csv " + es + " " + csv)                                         # Command variable for powershell terminal using Command line tools - https://github.com/neuromorphic-paris/command_line_tools)
subprocess.call('G:\\PG\\command_line_tools\\build\\release' + cmd, shell=True) # Run command

