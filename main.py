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

def update_ui_data():
    display.update_heading(current_data.heading)
    print(current_data.accelorometer)
    display.after(50, update_ui_data)



display = ui.AirplaneInstruments()
display.after(50, collect_data)
display.after(50, update_ui_data)
display.mainloop()

        
   

