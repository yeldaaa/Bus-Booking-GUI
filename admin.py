'''
Administrative functions.
These functions are generic and are used in many files.
'''

import csv
from time import sleep
import json

file_name = "accounts"
eachbuscap = 45 #assumed 45 seater capacity from NTU website

''' 
To load a csv file into Python, or create a new file if none exists.
Inputs:
    file_name - name of file (str)
    header_row - list of column names 
Output:
    Contents of the file
'''
def loadcsv(file_name,header_row):
    try:
        with open(f"{file_name}.csv","r",newline="") as file_pointer:
            csv_pointer = csv.reader(file_pointer)
            contents = list(csv_pointer) # returns a list of lists
    except FileNotFoundError:
        contents = [header_row]
        savecsv(contents,file_name,"w")
        
    return contents

'''
To save a csv file into the user's directory
Allows writing of multiple lines at once
Inputs:
    list_of_lists - list of lists of data to write into file 
'''
def savecsv(list_of_lists,file_name,mode):
    with open(f"{file_name}.csv",mode,newline="") as write_file:
        csv_pointer = csv.writer(write_file)
        csv_pointer.writerows(list_of_lists)

'''
Print a header; for decorative purposes only
Input: heading - the name to display (str)
'''
def header(heading):
    print("-"*10,heading,"-"*10)

'''
Lets user know that they are returning to menu.
'''    
def returntomenu():
    print("Returning to menu...\n")
    sleep(0.5)

'''
Loads bus json file into Python. Creates a new file if not found.
Format: data = {location: {time: [demand, capacity, waitlist]}} 
Input:
    filename - name of file (str)
Output:
    Contents of file
'''
def loadbusdata(filename):
    try:
        with open(f"{filename}.json","r") as fp:
            data = json.load(fp)
    except FileNotFoundError:
        # Info needs to be mutable. To avoid changing all instances of info when one changes,
        # need to make copies of the list
        info = [0,eachbuscap,0,0,0]
        data = {"name": "Data for NTU Heartland Services System",
                "meta": {
                        "Location": {
                                "Timing": "List of data: demand,capacity,students on waitlist,additional buses needed, add. buses sent"
                            }
                    },
                "data": 
                    {"Tampines": {"7:00": info.copy(),
                                 "7:10": info.copy()},
                    "Sengkang": {"7:00": info.copy(),
                                 "7:10": info.copy()},
                    "Punggol":  {"7:10": info.copy()},
                    "Ang Mo Kio": {"7:00": info.copy(),
                                   "7:10": info.copy(),
                                   "7:20": info.copy()},
                    "Bukit Gombak": {"7:40": info.copy(),
                                     "7:50": info.copy(),
                                     "8:00": info.copy()},
                    "Pasir Ris": {"7:00": info.copy()}
                    }
                }
        savebusdata(filename,data)
            
    return data

'''
Save bus json file into user's directory.
Inputs:
    filename - name of file (str)
    data - contents to save
'''
def savebusdata(filename, data):
    with open(f"{filename}.json","w") as write_file:
        json.dump(data,write_file,indent=4)
        
