### Dependencies
import pandas
import tkinter 
import subprocess
from tkinter import filedialog
from tkinter.filedialog import askopenfilenames


tkinter.Tk().withdraw()
file_paths = askopenfilenames()

### For loop to process multiple files in a single selection. Each CSV file (cf) in all of the files selected
for cf in file_paths:
    bf = cf[:-4]                                                            # remove .csv from file name in path - bare file (bf)       
    S_time = 4                                                              # Select a start time in seconds
    E_time = 7                                                              # Select a end time in seconds
    nfpcsv = bf + '_T' + str(S_time) + 'to' + str(E_time) + '.csv'          # New file name added to path (new file path csv - nfpcsv)
    nfpes = bf + '_T' + str(S_time) + 'to' + str(E_time) +'.es'             # New file name added to path (new file path es - nfpes)

    ### Zero CSV timestamps from shortened start and finish time and convert .csv to .es (Ncsv = New csv)
    Ncsv =  pandas.read_csv(cf)                                             # New csv is written with data from orginal file
    Ncsv['t'] -= (Ncsv['t'].iloc[0]-1)                                      # Zero time data incase not already reset
    filter = (Ncsv['t'] > (S_time*1e6)) & (Ncsv['t'] < (E_time*1e6))        # Filter for desired data using start and end time variables 
    Ncsv = Ncsv[filter]                                                     # Apply filter to New CSV
    Ncsv['t'] -= (Ncsv['t'].iloc[0]-1)                                      # Zero New time data
    Ncsv = Ncsv.dropna()                                                    # Remove any na rows 
    Ncsv.columns = ['t','x','y','on']                                       # Set CSV headers to t,x,y,on 
    Ncsv = Ncsv[:-1]                                                        # Data excluding last row 
    Ncsv.to_csv(nfpcsv, index = False)                                      # Create new CSV file in current location
    cmd = ("python G:\\PG\\CLT_CODE\\csv_to_es.py " + nfpcsv + " " + nfpes) # Variable for powershell command to convert csv file to es file (Command line tools - https://github.com/neuromorphic-paris/command_line_tools)
    subprocess.call(cmd)                                                    # Run powershell command


