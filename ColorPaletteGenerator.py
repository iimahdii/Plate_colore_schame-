from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from flask import Flask, jsonify, request
from colormath.color_objects import sRGBColor
import math
import random

app = Flask(__name__)

def generate_random_color():
    return sRGBColor(random.random(), random.random(), random.random(), is_upscaled=True)



def get_luminance(color):
    def channel_luminance(channel):
        if channel <= 0.03928:
            return channel / 12.92
        else:
            return ((channel + 0.055) / 1.055) ** 2.4

    r, g, b = [channel_luminance(channel) for channel in color.get_value_tuple()]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def calculate_contrast_ratio(color1, color2):
    l1 = get_luminance(color1)
    l2 = get_luminance(color2)

    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

def calculate_delta_e(color1, color2):
    lab1 = convert_color(color1, LabColor)
    lab2 = convert_color(color2, LabColor)
    delta_e = delta_e_cie2000(lab1, lab2)
    return delta_e

@app.route('/generate_palette', methods=['GET'])
def generate_palette():
    primary_color = generate_random_color()
    complementary_color = generate_random_color()  # Replace with actual logic for complementary color

    contrast_ratio = calculate_contrast_ratio(primary_color, complementary_color)
    delta_e = calculate_delta_e(primary_color, complementary_color)

    return jsonify({
        'primary_color': primary_color.get_upscaled_value_tuple(),
        'complementary_color': complementary_color.get_upscaled_value_tuple(),
        'contrast_ratio': contrast_ratio,
        'delta_e': delta_e
    })

if __name__ == '__main__':
    app.run(debug=True)
