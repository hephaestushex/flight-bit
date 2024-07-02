import time

from kaspersmicrobit import KaspersMicrobit


def pressed(button):
    print(f"button {button} pressed")

with KaspersMicrobit.find_one_microbit() as microbit:
    microbit.buttons.on_button_a(press=pressed)
    time.sleep(10)