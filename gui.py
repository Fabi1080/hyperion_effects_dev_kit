"""
This module is used to display the leds in a gui

Created on 27.11.2014

@author: Fabian Hertwig
"""
from Tkinter import *
import hyperion

_led_height = 20
_led_width = 20

master = Tk()


def rgb_to_string(r, g, b):
    # As defined by tkinter documentation
    return "#%02x%02x%02x" % (r, g, b)


def createWindow():
    # the empty window
    window_width = (hyperion.horizontal + 4) * _led_width
    window_height = (hyperion.vertical + 2) * _led_height
    canvas = Canvas(master, width=window_width, height=window_height)
    canvas.pack()

    # list for the led representing rectangles
    leds_without_offset = []

    # calculate positions of the rectangles
    x_increase = _led_width
    y_increase = _led_height
    x_pos = _led_width
    y_pos = 0

    # leave a space for the first corner led if necessary
    if not hyperion.corner_leds:
        x_pos += x_increase

    for i in range(hyperion.ledCount):
        rect = canvas.create_rectangle(x_pos, y_pos, x_pos + _led_width, y_pos + _led_height, fill="black",
                                       outline="white")
        leds_without_offset.append(rect)

        # Update the x and y pos so the result is a rectangle of single rectangles
        if i < hyperion.horizontal:
            # go one step to the right
            x_pos += x_increase
        elif i < hyperion.horizontal + hyperion.vertical:
            # go one step down
            y_pos += y_increase
        elif i < (2 * hyperion.horizontal) + hyperion.vertical:
            # go one step to the left
            x_pos -= x_increase
        elif i < (2 * hyperion.horizontal) + (2 * hyperion.vertical):
            # go one step up
            y_pos -= y_increase

        # Handle the corner leds
        if not hyperion.corner_leds:
            if i == hyperion.horizontal - 1:
                # At the top right corner, leave the space for the corner led empty
                y_pos += y_increase
            elif i == hyperion.horizontal + hyperion.vertical - 1:
                # At the bottom right corner, leave the space for the corner led empty
                x_pos -= x_increase
            elif i == 2 * hyperion.horizontal + hyperion.vertical - 1:
                # At the bottom left corner, leave the space for the corner led empty
                y_pos -= y_increase

    # Handle offset and counterclockwise led arrangement
    leds_with_direction = leds_without_offset[:]
    if not hyperion.clockwise_direction:
        # Reverse list but keep first entry (this is how hypercon does it)
        leds_with_direction = leds_without_offset[len(leds_without_offset):0:-1]
        leds_with_direction.insert(0, leds_without_offset[0])

    offset = hyperion.first_led_offset % hyperion.ledCount

    leds_with_offset = leds_with_direction[offset:]
    leds_with_offset.extend(leds_with_direction[:offset])

    # Call master which recalls itself to update the gui in the mainloop
    master.after(33, update_leds, canvas, leds_with_offset)
    mainloop()


def update_leds(canvas, leds_with_offset):
    for i in range(len(leds_with_offset)):
        change_color(canvas, leds_with_offset[i], i)

    master.after(33, update_leds, canvas, leds_with_offset)


def change_color(canvas, rect, led_number):
    led_data_copy = hyperion.get_led_data()
    if len(led_data_copy) >= 3 * led_number + 2:
        r = hyperion.get_led_data()[3 * led_number + 0]
        g = hyperion.get_led_data()[3 * led_number + 1]
        b = hyperion.get_led_data()[3 * led_number + 2]

        canvas.itemconfigure(rect, fill=rgb_to_string(r, g, b))