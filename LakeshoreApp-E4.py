# -*- coding: utf-8 -*-
"""
FileName:  LakeshoreApp-E4.py 808 500 690

Created on Mon Sep 18 19:12:32 2023
modified 12/7/2023 to 30 sec sample rate 

@author: ahh


"""
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
from lakeshore import *
from lakeshore.model_336 import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from datetime import datetime
import time

global OutFile, FileName, Timing

Timing = 30000 # interval in milliseconds 

# root window
root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('FileName')

# store default placeholder filename 
filename = tk.StringVar(root,value='CET#####')

def login_clicked():
    """ callback when the login button clicked
    """
    global FileName, OutFile
    FileName = f'{filename.get()}'
    #msg = f'You entered: {filename.get()} '
    #showinfo(
    #    title='Information',
    #   message=msg)
    print('FileName = ', FileName)

    #    'C:\\Users\\User Access\\Desktop\\Test lab files sync\\'

    OutFile = 'C:\\Users\\User Access\\Desktop\\Test Lab Files Sync\\' + FileName + '.csv'    
    print('OutFile = ', OutFile)
    root.destroy()


# Sign in frame
signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)


# filename
filename_label = ttk.Label(signin, text="FileName:")
filename_label.pack(fill='x', expand=True)

filename_entry = ttk.Entry(signin, textvariable=filename)
filename_entry.pack(fill='x', expand=True)
filename_entry.focus()

def Fetch_Button():
# login button
    global OutFile
    login_button = ttk.Button(signin, text="Enter", command=login_clicked)
    login_button.pack(fill='x', expand=True, pady=10)


Fetch_Button()

if __name__ == '__main__': root.mainloop()

# ----------------------------------------------------------------------------
dt = datetime.now()

    #    'C:\\Users\\User Access\\Desktop\\Test lab files sync\\'

NoteFileName = 'C:\\Users\\User Access\\Desktop\\Test Lab Files Sync\\' + FileName + '_Notes.txt'

def extract_data():
    global Notes
    Notes = (text_box.get('1.0', 'end'))
    print(Notes)
    with open(NoteFileName, 'w') as f:
        f.writelines(Notes)
    root.destroy()

def clear_textbox():
    text_box.delete(1.0, 'end')

root = Tk()
root.title('Notes')
root.geometry('500x300')
root.config(bg='#F0F0F0')

message = dt.strftime('%x %X\n') + OutFile + '''

'''

frame = Frame(root)

text_box = Text(
    frame,
    height=15,
    width=50,
    font=('Ariel',10),
    wrap='word'
)
text_box.insert('end', message)
text_box.pack(side=LEFT,expand=True)


sb = Scrollbar(frame)
sb.pack(side=RIGHT, fill=BOTH)

text_box.config(yscrollcommand=sb.set)
sb.config(command=text_box.yview)

frame.pack(expand=True)

Button(
    root,
    text='Clear',
    width=15,
    height=2,
    command=clear_textbox
).pack(side='left', expand=True)

Button(
    root,
    text='Save Notes',
    width=15,
    height=2,
    command=extract_data
).pack(side='right', expand=True)

root.mainloop()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------

#  Read Termperature

LAKESHORE_336_IP = '172.16.65.150'

numframes = 432000  # 60 sec x 60 min x 24 hours = 86400
                    # 5 days = 432,000 sec
                    # Repeat interval for x-axis plot 
def Read_336():
    global tA, tB, tC, tD, temp

    M336 = Model336(ip_address=LAKESHORE_336_IP)
    M336.connect_tcp(ip_address=LAKESHORE_336_IP, tcp_port=7777, timeout=2.0)
    tA = round(float(M336.query('KRDG? A')),3)
    tB = round(float(M336.query('KRDG? B')),3)
    tC = round(float(M336.query('KRDG? C')),3)
    tD = round(float(M336.query('KRDG? D')),3)
    
    temp = tA, tB, tC, tD
    print(temp)
    return(temp)
    M336.disconnect_tcp()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# Initialize empty lists to store data
x_data = []
y_data = [[] for _ in range(4)]  # Create lists for each line

# Create a figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlim(-5, 200 + 5) # x limit intially now set to 200 min
ax.set_ylim(0, 400)
ax.set_ylabel('Temperature [K]')
ax.set_xlabel('Time since start [m]')
ax.set_title('Temperature Measurement\n' + OutFile)
ax.grid(visible=True, which='major')

# Create lines for temperature sensors and the new function
lines = []
colors = ['#00A5D1', '#990000', '#009900', '#006666']
labels = ['Sensor A', 'Sensor B', 'Sensor C', 'Sensor D']

for i in range(4):
    line, = ax.plot([], [], lw=2, label=labels[i], color=colors[i])
    lines.append(line)


# Add a legend
ax.legend(lines, labels)


def init():
    for line in lines:
        line.set_data([], [])
    return lines

start_time = time.strftime('%H:%M:%S')
start = time.time()

def animate(i):
    # Update temperature data
    Read_336()

    
    x = i

    rltime = time.strftime('%H:%M:%S')
    end = time.time()
    elapsed_time = (end - start)/60  #elapsed time in minutes (seconds/60)
    print(f" {rltime}, {x}, {elapsed_time:.2f}")    

    x_data.append(elapsed_time)

    
    for j in range(4):
        y = temp[j]   #if j < 3 else fA
        y_data[j].append(y)
        lines[j].set_data(x_data, y_data[j])

    return lines


ani = FuncAnimation(fig, animate, frames=numframes, interval=Timing) # interval in ms

# Create a CSV file to save the data
csv_filename = OutFile

# Function to save data to CSV after the animation is complete
def save_data_to_csv(event=None):  # Accept an optional event argument
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Time'] + labels
        writer.writerow(header)
        
        for i in range(len(x_data)):
            row = [x_data[i]] + [y_data[j][i] for j in range(4)]
            writer.writerow(row)

# Add a callback to save data when the animation is finished
ani.event_source.add_callback(save_data_to_csv)

# Show the plot
plt.show()

