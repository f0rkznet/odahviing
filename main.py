import time
import board
import neopixel
import random
import numpy as np

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
        (190, 219, 57),
        (168, 197, 69),
        (189, 214, 132),
        (150, 202, 45),
        (40, 153, 118)

    ],
    'medium': [(0,0,0), (0,0,255)],
    'high': [(0,0,0), (255,0,0)],
}

def fire_cycle(heat):
    for pixel in range(num_pixels):
        pixels[pixel] = random.choice(heat)
        pixels.show()
        time.sleep(random.choice(np.arange(0.0, 1.0, 0.01)))

if __name__ == '__main__':
    while True:
        fire_cycle(heat=heatmap['low'])
