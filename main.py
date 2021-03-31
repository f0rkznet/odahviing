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

heatmap = {
    'low': [
        (0,0,0),
        (0, 38, 28),
        (22, 128, 57),
        (69, 191, 85),
        (150, 237, 137),
        (0,255,0),
    ],
    'medium': [
        (0,0,0),
        (0, 48, 90),
        (0, 75, 141),
        (0, 116, 217),
        (65, 146, 217),
        (122, 186, 242),
        (0,0,255),
    ],
    'high': [
        (0,0,0),
        (69, 0, 3),
        (92, 0, 2),
        (148, 9, 13),
        (212, 13, 18),
        (255, 29, 35),
        (255,0,0),
    ],
}

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
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

def rainbow_cycle():
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()

def fire_cycle(heat):
    for pixel in range(num_pixels):
        pixels[pixel] = random.choice(heat)
        pixels.show()
        time.sleep(random.choice(np.arange(0.0, 0.5, 0.01)))

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
    print(port_data['ifInOctets_rate'])

    in_rate = port_data['ifInOctets_rate'] * 8 / if_speed * 100

    print('{} Mbit/s'.format(in_rate))
    if in_rate <= 100:
        return('low')
    elif in_rate <= 500 and in_rate > 100:
        return('medium')
    elif in_rate <= 1100 and in_rate > 500:
        return('high')
if __name__ == '__main__':
    while True:
        rainbow_cycle()
        heat = get_port_heat(LIBRENMS_PORT)
        fire_cycle(heat=heatmap[heat])
