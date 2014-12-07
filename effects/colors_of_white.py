"""
import hyperion
import time
import colorsys
import random

# Get the parameters
change_speed = float(hyperion.args.get('change_speed', 1.0))
saturation_min = float(hyperion.args.get('saturation_min', 0.1))
saturation_max = float(hyperion.args.get('saturation_max', 0.3))

hue_increment = 0.01
hue_tendency = 0.0002
sat_increment = 0.002

sleepTime = 0.2

random.seed(time.time())
baseHsv = [0.0, 0.0, 1.0]


while not hyperion.abort():
    # Move the hue and saturation randomly.
    # random between -1.0 and 1.0
    ran = ((random.random() * 2) - 1)
    baseHsv[0] += ran * hue_increment * change_speed + hue_tendency
    baseHsv[0] %= 1.0
    # random between -1.0 and 1.0
    ran = ((random.random() * 2) - 1)
    saturation = baseHsv[1] + ran * sat_increment * change_speed
    # clamp between min and max
    baseHsv[1] = max(saturation_min, min(saturation_max, saturation))
    rgb = colorsys.hsv_to_rgb(baseHsv[0], baseHsv[1], baseHsv[2])

    # set colors
    led_data = bytearray()
    for i in range(hyperion.ledCount):
        led_data += bytearray((int(255*rgb[0]), int(255*rgb[1]), int(255*rgb[2])))

    hyperion.setColor(led_data)

    # sleep for a while
    time.sleep(sleepTime)

    print baseHsv

"""