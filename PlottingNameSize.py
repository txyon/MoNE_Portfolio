### Dependencies
import os
import numpy
import pandas
import tkinter
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames

tkinter.Tk().withdraw()
file_paths = askopenfilenames()
csv = pandas.DataFrame(columns=["File","Size"])                         #Establish variable for csv dataframe

### Loop for processing multiple files in a single batch
for f in file_paths:
    name = os.path.basename(f)                                          # Get file name
    name = name[:-10]                                                   # Remove unwanted characters from selected file name can adjust or comment out
    size = os.path.getsize(f)                                           # Get file size in kilobytes
    size = size/(1024*1024)                                             # Size in bytes convert to MB
    csv = pandas.concat([csv, pandas.DataFrame({"File": [name], "Size": [size]})], ignore_index=True)
                                                                        # LINE ABOVE # Add file and size data to csv variable

#csv.to_csv("Diff_On_File_Size_255_156.csv", index = False)             # Write to CSV (On files)
csv.to_csv("Diff_Off_File_Size_155_48.csv", index = False)              # Write to CSV (Off files)

plt.plot(csv['File'], csv['Size'], marker='o', linestyle='-', color='b')# Line graph config
plt.gca().invert_xaxis()                                                # Invert X Axis 
plt.grid(True)                                                          # Display grid in plot
plt.xlabel('File')                                                      # X label
plt.ylabel('Size(MB)')                                                  # Y Label
#plt.title('Diff_On 255<>156 File Size Line Graph')                     # Title (On)
plt.title('Diff_Off 155<>48 File Size Line Graph')                      # Title (Off)
plt.xticks(rotation=90)                                                 # Turn x labels 90 deg

plt.show()                                                              # Display plot
