# -*- coding: utf-8 -*-
"""
FileName:  Flow.py 808 500 690

Created on Mon Sep 18 19:12:32 2023
modified 11/17/2023 to add COM port input box, Yellow LED alternates
modified 12/7/2023 to 30 sec sample rate

@author: ahh

Flow mapped to comPort

"""
import serial
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from datetime import datetime
import time

# Set the Matplotlib backend to TkAgg
matplotlib.use('TkAgg')

global comPort, LED, Timing

Timing = 30000 # interval in milliseconds


# ----------------------------------------------------------------------------

global comPort, LED

Timing = 30000 # interval in milliseconds

LED = False

# root window
root = tk.Tk()
root.geometry("300x150")
root.resizable(False, False)
root.title('comPort')


# store default placeholder comPort 
comport = tk.StringVar(root,value='COM3')

def is_valid_com_port(port):
    try:
        ser = serial.Serial(port)
        ser.close()
        return True
    except serial.SerialException:
        return False

def login_clicked():
    """ callback when the login button clicked
    """
    global comPort
    comPort = f'{comport.get()}'
   
    print('comPort = ', comPort)
 
    if is_valid_com_port(comPort):
        print(f"{comPort} is a valid COM port.")

    else:
        msg = f'{comPort} is not a valid COM Port'
        showinfo(
            title='Information',
            message=msg)
        print(f"{comPort} is not a valid COM port")        
        raise KeyboardInterrupt
        
    root.destroy()

# Sign in frame
signin = ttk.Frame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)


# comPort
comPort_label = ttk.Label(signin, text="Enter comPort for Flow:")
comPort_label.pack(fill='x', expand=True)

comPort_entry = ttk.Entry(signin, textvariable=comport)
comPort_entry.pack(fill='x', expand=True)
comPort_entry.focus()

def Fetch_Button():
# login button
    login_button = ttk.Button(signin, text="Enter", command=login_clicked)
    login_button.pack(fill='x', expand=True, pady=10)


Fetch_Button()
if __name__ == '__main__': root.mainloop()


# ----------------------------------------------------------------------------

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

    #    'C:\\CET\\Test lab files sync\\'
    #    'C:\\Test Data\\Test Lab Files Sync\\'

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

    #    'C:\\CET\\Test lab files sync\\'
    #    'C:\\Test Data\\Test Lab Files Sync\\'

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

numframes = 432000  # 60 sec x 60 min x 24 hours = 86,400
                    # 5 days = 432,000 sec
                    # Repeat interval for x-axis plot 

line = 'A,0,0'
saved_line = line.encode('ascii')

Flow = ""
fA = 1.0
fB = 1.0

def Config_Flow():

#    print(cport)

    ser = serial.Serial(port=comPort,
                    baudrate=57600,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

    Byte_Flow = ('C,3,0,0,2\n')
#    print(Byte_Flow)
    ser.write(Byte_Flow.encode('ascii'))
    line = ser.readline()
    Answer = line.decode('ascii')
    print(Answer)

def Read_Flow():
    global fA, fB, line, saved_line, LED

#    print('Flow assigned to ', comPort)

    ser = serial.Serial(port=comPort,
                    baudrate=57600,
                    bytesize=8,
                    parity='N',
                    stopbits=1)

    if LED:
        Byte_Flow = ('PO,C,7,0\n') # Set Yellow LED OFF
        LED = False
    else:
        Byte_Flow = ('PO,C,7,1\n') # Set Yellow LED ON
        LED = True
#    print(Byte_Flow)
    ser.write(Byte_Flow.encode('ascii'))
    line = ser.readline()
    Answer = line.decode('ascii')
#    print(Answer)    
    
    
    Byte_Flow = ('A\n')
#    print(Byte_Flow)
    ser.write(Byte_Flow.encode('ascii'))
    line = ser.readline()
#    print('line = ', line)
    
    #need to test that line is not "ok" 
    
    if (line.decode('ascii') == 'ok\r\n'):
        line = saved_line
        print('line saved')
    
    Flow = line.decode('ascii')
    saved_line = line
#    print('saved_line = ', saved_line)
#    print(Flow)
    fA = round(float(Flow.split(",")[1]) * 20.0 / 1024.0, 1)
    fB = round(float(Flow.split(",")[2]) * 20.0 / 1024.0, 1)
    return(fA, fB)

Config_Flow()

# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# Initialize empty lists to store data
x_data = []
y_data = [[] for _ in range(2)]  # Create lists for each line

# Create a figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlim(-5, 200 + 5) # x limit intially now set to 200 minutes
ax.set_ylim(0, 25)
ax.set_ylabel('Flow [l/min]')
ax.set_xlabel('Time since start [m]')
ax.set_title('Flow Measurement\n' + OutFile)
ax.grid(visible=True, which='major')
ax.tick_params(axis='y', labelcolor='#660099')  # Purple

# Create lines for  the new function
lines = []
colors = ['#00A5D1', '#660099']
labels = ['Flow A', 'Flow B']
'''
    line, = ax.plot([], [], lw=2, label=labels[i], color=colors[i])
    lines.append(line)


# Add a second y-axis on the right side of the plot
ax2 = ax.twinx()
ax2.set_ylim(0, 25)  # Adjust the y-limits for Flow A

# Add a second ylabel for Line 5
ax2.set_ylabel('Flow B', color='#660099')  # Purple

'''
# Create lines for the new function (example: a sine wave)
FlowA, = ax.plot([], [], lw=2, label='Flow A', color='#660099')  # Purple
FlowB, = ax.plot([], [], lw=2, label='Flow B', color='#FF0000')  # Red

# Add Flow to the lines list
lines.append(FlowA)
lines.append(FlowB)

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
    Read_Flow()
    
    x = i

    rltime = time.strftime('%H:%M:%S')
    end = time.time()
    elapsed_time = (end - start)/60  #elapsed time in minutes (seconds/60)
    print(f" {rltime}, {x}, {elapsed_time:.2f}, {fA}, {fB}")    

    x_data.append(elapsed_time)

    y_data[0].append(fA)
    y_data[1].append(fB)

    # Update the line objects with new data
    lines[0].set_data(x_data, y_data[0])
    lines[1].set_data(x_data, y_data[1])

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
            row = [x_data[i]] + [y_data[j][i] for j in range(2)]
            writer.writerow(row)

# Add a callback to save data when the animation is finished
ani.event_source.add_callback(save_data_to_csv)

# Show the plot
plt.show(block=False)  # Set block=False to allow interaction

# Call the root.mainloop() after the plot is shown
root.mainloop()

