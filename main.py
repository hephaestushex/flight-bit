#modules for proper bluetooth connection
from kaspersmicrobit import *
from kaspersmicrobit.services.magnetometer import *
from kaspersmicrobit.services.accelerometer import *

#ui dependencies
import tkinter as tk
import math

#finally import the ui class from the other file
import ui


#create a data type for easy data collection
class ui_data:
    def __init__(self, heading, accelerometer):
        self.heading = heading
        self.accelerometer = accelerometer

#create the data variable
global current_data
current_data = ui_data(0, 0)

#funtion to collect data
def collect_data():
        microbit = KaspersMicrobit.find_one_microbit() # define microbit in variable
        
        try: #run code to collect data
            microbit.connect()
            current_data.heading = microbit.magnetometer.read_bearing()
            current_data.accelorometer = microbit.accelerometer.read()
        finally: #disconnect microbit
            microbit.disconnect()
        #call the function again
        display.after(50, collect_data)

#function to calibrate micro:bit
def calibrate_flight_bit():
    microbit = KaspersMicrobit.find_one_microbit()
    try:
        microbit.connect()
        calibration = microbit.magnetometer.calibrate()
        print("Calibrating...")

        #Wait for the calibration to finish
        if calibration.wait_for_result():
           print("Calibration succes!")
        else:
            print("Calibration failed!")
        
    finally:
        microbit.disconnect()

#calculate pitch and roll from raw accelerometer data
def calculate_pitch_roll(x, y, z):
    pitch = math.atan2(y, math.sqrt(x**2 + z**2))
    roll = math.atan2(x, math.sqrt(y**2 + z**2))

    pitch = math.degrees(pitch)
    roll = math.degrees(roll)
    
    return pitch, roll

def update_ui_data():
    display.update_heading(current_data.heading) #show heading
    
    #change data from milli-gs to gs
    x, y, z = current_data.accelorometer.x / 1000, current_data.accelorometer.y / 1000, current_data.accelorometer.z / 1000

    #calculate pitch and roll from updated gs
    pitch, roll = calculate_pitch_roll(x, y, z)
    display.update_attitude(math.floor(pitch), math.floor(roll)) # finally display data and rounding it
    display.after(50, update_ui_data) # call this funcion again


#loop
display = ui.AirplaneInstruments()
#display.after(1, calibrate_flight_bit) #runs this once per session of flight:bit. comment this out for testing
display.after(50, collect_data)
display.after(50, update_ui_data)
display.mainloop()

        
   

