import time
import board
import neopixel
import random
import numpy as np
import os
import requests

LIBRENMS_URL   = os.environ.get('LIBRENMS_URL', None)
LIBRENMS_TOKEN = os.environ.get('LIBRENMS_TOKEN', None)
LIBRENMS_PORT  = os.environ.get('LIBRENMS_PORT', None)

pixel_pin = board.D18
num_pixels = 12
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin,
    num_pixels,
    auto_write=False,
    pixel_order=ORDER,
)

def blue_dragon(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = 0
        g = 0
        b = int(pos * 3)
    elif pos < 170:
        pos -= 85
        r = 0
        g = 0
        b = int(255 - pos * 3)
    else:
        pos -= 170
        r = 0
        g = 0
        b = int(pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def earth_dragon(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = 0
        g = int(255 - pos * 3)
        b = int(pos * 3)
    elif pos < 170:
        pos -= 85
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(255 - pos * 3)
        b = int(pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def green_dragon(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = 0
        g = int(pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = 0
        g = int(255 - pos * 3)
        b = 0
    else:
        pos -= 170
        r = 0
        g = 0
        b = 0
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def red_dragon(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = 0
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = 0
    else:
        pos -= 170
        r = 0
        g = 0
        b = 0
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def chromatic_dragon(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def chromatic_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = chromatic_dragon(pixel_index & 255)
        pixels.show()

def blue_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = blue_dragon(pixel_index & 255)
        pixels.show()

def fire_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = red_dragon(pixel_index & 255)
        pixels.show()

def green_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = green_dragon(pixel_index & 255)
        pixels.show()

def earth_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = earth_dragon(pixel_index & 255)
        pixels.show()

def get_port_heat(port):
    request_uri = '{}api/v0/ports/{}'.format(
        LIBRENMS_URL,
        port
    )
    headers = {'X-Auth-Token': LIBRENMS_TOKEN}
    r = requests.get(url=request_uri, headers=headers)

    port_data = r.json()
    port_data = port_data['port'][0]
    if_speed = port_data['ifSpeed']

    in_rate = port_data['ifInOctets_rate'] * 8 / if_speed * 100

    if in_rate <= 33:
        return('low')
    elif in_rate <= 66 and in_rate > 33:
        return('medium')
    elif in_rate <= 100 and in_rate > 66:
        return('high')

if __name__ == '__main__':
    while True:
        # rainbow_cycle()
        # heat = get_port_heat(LIBRENMS_PORT)
        # fire_cycle(heat=heatmap[heat])
        # ice_cycle()
        # fire_cycle()
        # green_cycle()
        for i in range(10):
            earth_cycle()
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(2)
        for i in range(10):
            chromatic_cycle()
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(2)
        for i in range(10):
            blue_cycle()
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(2)
        for i in range(10):
            fire_cycle()