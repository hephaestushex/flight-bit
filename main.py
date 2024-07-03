from kaspersmicrobit import KaspersMicrobit
import kaspersmicrobit.services.magnetometer
import time
import tkinter as tk
import math
from ui import AirplaneInstruments

recieving_data = False

def pressed(button):

    if button == "A":
        recieving_data = True
        print("flight:bit is sending data!")

    if button == "B":
        recieving_data = False
        print("flight:bit is no longer sending data :( ")

with KaspersMicrobit.find_one_microbit() as microbit:
    
    microbit.buttons.on_button_a(press=pressed)
    microbit.buttons.on_button_b(press=pressed)

    


    ui = AirplaneInstruments

    

    while True:
        ui.update_heading(read_bearing())
        ui.mainloop()
   

