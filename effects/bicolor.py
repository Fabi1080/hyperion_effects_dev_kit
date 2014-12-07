"""
import hyperion
import time
import colorsys

# Get the parameters
change_speed = float(hyperion.args.get('change_speed', 1.0))
saturation_min = float(hyperion.args.get('saturation_min', 0.1))
saturation_max = float(hyperion.args.get('saturation_max', 0.3))
offset = 13
rotation_speed = 0.01
sleepTime = 0.1
color1_change = 0.001
color2_change = 0.0013


def blend_function(rgb1, rgb2, percent):
    rgb_result = [0, 0, 0]
    rgb_result[0] = blend_one_color(rgb1[0], rgb2[0], percent)
    rgb_result[1] = blend_one_color(rgb1[1], rgb2[1], percent)
    rgb_result[2] = blend_one_color(rgb1[2], rgb2[2], percent)
    return rgb_result


def blend_one_color(c1, c2, percent):
    return (1.0 - percent) * c1 + percent * c2


blend_percantages = []

for i in range(hyperion.ledCount):
    if i < hyperion.ledCount / 2.0:
        blend_percantages.append((i * 1.0) / (hyperion.ledCount / 2.0))
    else:
        blend_percantages.append((hyperion.ledCount - i * 1.0) / (hyperion.ledCount / 2.0))

blend_percantages = blend_percantages[-offset:] + blend_percantages[:-offset]

rotation = 0
rgb1 = [255, 100, 100]
rgb2 = [100, 100, 255]

hsv1 = list(colorsys.rgb_to_hsv(rgb1[0] / 255.0, rgb1[1] / 255.0, rgb1[2] / 255.0))
hsv2 = list(colorsys.rgb_to_hsv(rgb2[0] / 255.0, rgb2[1] / 255.0, rgb2[2] / 255.0))

while not hyperion.abort():

    # set colors
    led_data = bytearray()
    blend_percantages_rotated = blend_percantages[-1 * int(rotation):] + blend_percantages[:-1 * int(rotation)]

    for i in range(hyperion.ledCount):
        blend = blend_function(rgb1, rgb2, blend_percantages_rotated[i])
        led_data += bytearray((int(blend[0]), int(blend[1]), int(blend[2])))

    hyperion.setColor(led_data)

    # set rotation
    rotation = (rotation + rotation_speed) % hyperion.ledCount

    # change colors
    # change hue
    hsv1[0] = (hsv1[0] + color1_change) % 1.0
    hsv2[0] = (hsv2[0] + color2_change) % 1.0
    # convert to rgb
    rgb1 = list(colorsys.hsv_to_rgb(hsv1[0], hsv1[1], hsv1[2]))
    rgb2 = colorsys.hsv_to_rgb(hsv2[0], hsv2[1], hsv2[2])
    # convert rgb 0..1 to rgb 0..255
    rgb1 = [int(c * 255) for c in rgb1]
    rgb2 = [int(c * 255) for c in rgb2]

    # sleep for a while
    time.sleep(sleepTime)



"""