import hyperion
import time
import colorsys

""" Get the parameters defined in the json file. The value at the end is used if it the data is not found """
a_float = float(hyperion.args.get('a_float', 20.0))
other = hyperion.args.get('other', (0, 0, 255))
a_int = int(hyperion.args.get('a_int', 5))
a_bool = bool(hyperion.args.get('a_bool', False))

""" Define some variables """
sleepTime = 0.2

offset = 17
blend_percantages = []
rotation = 0
""" these should be in the json file so the user can manipulate them """
rotation_speed = 0.001
color1_change = 0.0001
color2_change = 0.00011
rgb1 = [255, 100, 100]
rgb2 = [100, 100, 255]


""" Define some functions """
def blend_function(rgb1, rgb2, percent):
    rgb_result = [0, 0, 0]
    rgb_result[0] = blend_one_color(rgb1[0], rgb2[0], percent)
    rgb_result[1] = blend_one_color(rgb1[1], rgb2[1], percent)
    rgb_result[2] = blend_one_color(rgb1[2], rgb2[2], percent)
    return rgb_result


def blend_one_color(c1, c2, percent):
    return (1.0 - percent) * c1 + percent * c2

""" Precalculate stuff """
for i in range(hyperion.ledCount):
    if i < hyperion.ledCount / 2.0:
        blend_percantages.append((i * 1.0) / (hyperion.ledCount / 2.0))
    else:
        blend_percantages.append((hyperion.ledCount - i * 1.0) / (hyperion.ledCount / 2.0))

blend_percantages = blend_percantages[-offset:] + blend_percantages[:-offset]

hsv1 = list(colorsys.rgb_to_hsv(rgb1[0] / 255.0, rgb1[1] / 255.0, rgb1[2] / 255.0))
hsv2 = list(colorsys.rgb_to_hsv(rgb2[0] / 255.0, rgb2[1] / 255.0, rgb2[2] / 255.0))

""" The effect loop """
while not hyperion.abort():

    """ The algorithm to calculate the change in color """
    led_data = bytearray()
    blend_percantages_rotated = blend_percantages[-1 * int(rotation):] + blend_percantages[:-1 * int(rotation)]

    for i in range(hyperion.ledCount):
        blend = blend_function(rgb1, rgb2, blend_percantages_rotated[i])
        led_data += bytearray((int(blend[0]), int(blend[1]), int(blend[2])))

    """ send the data to hyperion """
    hyperion.setColor(led_data)

    """ do any other stuff that needs to be done afterwards """
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

    """ sleep for a while """
    time.sleep(sleepTime)



