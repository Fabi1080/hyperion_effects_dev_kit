"""
This module is used to send the led data to hyperion's json server

Created on 27.11.2014

@author: Fabian Hertwig
"""

import socket

s = None
connected = False


def open_connection(host, port, timeout=10):
    """
    Open a socket connection to the server
    :param host: Hostname oder ip address of the server
    :param port: Port of the server
    :param timeout: timeout in seconds
    """
    global connected
    global s

    if connected:
        return

    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        connected = True
    except socket.error, exc:
        print "Error on connection to ", host, ":", port, "\nMessage: ", exc


def close_connection():
    if connected:
        try:
            s.send('{"command":"clearall"}\n')
            s.close()
        except socket.error, exc:
            print "Could not close socket connection\nMessage: ", exc


def send_led_data(led_data):
    """
    Send the led data in a message format the hyperion json server understands
    :param led_data: bytearray of the led data (r,g,b) * hyperion.ledcount
    """
    if not connected:
        return
    # create a message to send
    message = '{"color":['
    # add all the color values to the message
    for i in range(len(led_data)):
        message += repr(led_data[i])
        # separate the color values with ",", but do not add a "," at the end
        if not i == len(led_data) - 1:
            message += ','
    # complete message
    message += '],"command":"color","priority":100}\n'
    try:
        s.send(message)
    except socket.error, exc:
        print "Error while sending the led data\nMessage: ", exc