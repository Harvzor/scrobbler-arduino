from time import sleep
from machine import Pin

import api
from display import display, graphics, menu
import wifi
import bt

# https://micronote.tech/2020/02/Timers-and-Interrupts-with-a-NodeMCU-and-MicroPython/
def debounce(pin):
    prev = None
    for _ in range(100):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
    return prev

def show_health(health):
    display.fill(0)

    if health.is_healthy():
        display.text('API healthy', 0, 20)
    else:
        display.text('API unhealthy!', 0, 20)

    display.show()

def load_and_show_trackables_menu():
    trackables = api.get_trackables()

    display.fill(0)

    text = []

    for trackable in trackables:
        text.append([trackable.name, 'scrobble_item(' + str(trackable.id) + ')'])

    menu.initText(text)

    display.show()

def scrobble_item(item_id):
    display.fill(0)

    display.text('Scrobbling...', 0, 20)

    display.show()

    scrobble = api.post_scrobble(item_id)

    if scrobble == None:
        display.text('Something went wrong', 0, 30)
        display.show()
    else:
        display.text('Done!', 0, 30)
        display.show()

    sleep(3)

    load_and_show_trackables_menu()

def button_up_callback(pin):
    d = debounce(pin)

    if d == None:
        return
    elif d:
        # print('up')
        # print(pin.value())

        # display.fill(0)
        # display.text('Up', 0, 0)
        # display.show()

        menu.moveUp()
        display.show()
    else:
        return

def button_down_callback(pin):
    d = debounce(pin)

    if d == None:
        return
    elif d:
        # print('down')
        # print(pin.value())

        # display.fill(0)
        # display.text('Down', 0, 0)
        # display.show()

        menu.moveDown()
        display.show()
    else:
        return

def button_select_callback(pin):
    d = debounce(pin)

    if d == None:
        return
    elif d:
        # print('click')
        # print(pin.value())

        # display.fill(0)
        # display.text('Click', 0, 0)
        # display.show()

        menu.click()
    else:
        return

def setup_buttons():
    global button_up
    global button_down
    global button_select

    button_up = Pin(23, Pin.IN, Pin.PULL_UP)
    button_down= Pin(19, Pin.IN, Pin.PULL_UP)
    button_select = Pin(22, Pin.IN, Pin.PULL_UP)

    button_up.irq(trigger = Pin.IRQ_RISING, handler = button_up_callback)
    button_down.irq(trigger = Pin.IRQ_RISING, handler = button_down_callback)
    button_select.irq(trigger = Pin.IRQ_RISING, handler = button_select_callback)

def main():
    bt.demo()

    wifi.do_connect()

    setup_buttons()

    health = api.get_health()
    show_health(health)

    if health.is_healthy():
        load_and_show_trackables_menu()

main()
