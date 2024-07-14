from kaspersmicrobit import *
from kaspersmicrobit.services.magnetometer import *
from kaspersmicrobit.services.accelerometer import *

import time

import tkinter as tk
import math

import ui



class ui_data:
    def __init__(self, heading, accelerometer):
        self.heading = heading
        self.accelorometer = accelerometer

global current_data
current_data = ui_data(0, 0)


def collect_data():
        microbit = KaspersMicrobit.find_one_microbit()
        
        try:
            microbit.connect()
            current_data.heading = microbit.magnetometer.read_bearing()
            current_data.accelorometer = microbit.accelerometer.read()
            print("collected")
        finally:
            microbit.disconnect()
        
        display.after(50, collect_data)


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

def calculate_pitch_roll(x, y, z):
    pitch = math.atan2(y, math.sqrt(x**2 + z**2))
    roll = math.atan2(x, math.sqrt(y**2 + z**2))

    pitch = math.degrees(pitch)
    roll = math.degrees(roll)
    
    return pitch, roll

def update_ui_data():
    display.update_heading(current_data.heading)
    
    x, y, z = current_data.accelorometer.x / 1000, current_data.accelorometer.y / 1000, current_data.accelorometer.z / 1000

    pitch, roll = calculate_pitch_roll(x, y, z)
    display.update_attitude(math.floor(pitch), math.floor(roll))
    display.after(50, update_ui_data)



display = ui.AirplaneInstruments()
#display.after(1, calibrate_flight_bit) #runs this once per session of flight:bit. comment this out for testing
display.after(50, collect_data)
display.after(50, update_ui_data)
display.mainloop()

        
   

