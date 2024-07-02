from kaspersmicrobit import KaspersMicrobit
import time

recieving_data = False

def pressed(button):

    if button == "A":
        recieving_data = True
        print(recieving_data)

    if button == "B":
        recieving_data = False
        print(recieving_data)

with KaspersMicrobit.find_one_microbit() as microbit:
    # listen for button events / luister naar drukken op knoppen
    microbit.buttons.on_button_a(press=pressed)
    microbit.buttons.on_button_b(press=pressed)
    time.sleep(15)