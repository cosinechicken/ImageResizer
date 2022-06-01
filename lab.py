#!/usr/bin/env python3

import math

from PIL import Image as Image

# Get the pixel at (x,y)
def get_pixel(image, x, y):
    return image['pixels'][x * image['width'] + y]

def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': [],
    }
    # Go through all pixels in order and apply correlation on them and return the result
    for i in range(image['height']):
        for j in range(image['width']):
            pixel = get_pixel(image, i, j)
            # clip the pixel
            if pixel > 255:
                pixel = 255
            if pixel < 0:
                pixel = 0
            # round the pixel
            pixel = round(pixel)
            # add the pixel in
            result['pixels'].append(pixel)

    return result


# FILTERS

def resized(size_tuple):
    # helper function for calling color_filter_from_greyscale_filter on resized_temp
    width, height = size_tuple
    def ans(image):
        return resized_temp(image, width, height)
    return ans

def resized_temp(image, width, height):
    result = {
        'height': height,
        'width': width,
        'pixels': [],
    }
    # Calculate the answer for each pixel and add it into result
    for x in range(height):
        for y in range(width):
            x_start = image['height']*x/height
            x_end = image['height']*(x+1)/height
            y_start = image['width'] * y / width
            y_end = image['width'] * (y + 1) / width

            sum = 0
            cur_x = math.floor(x_start)
            while cur_x < x_end:
                cur_y = math.floor(y_start)
                while cur_y < y_end:
                    # find the x_multiplier
                    x_multiplier = 1
                    if cur_x == math.floor(x_start):
                        x_multiplier -= (x_start - math.floor(x_start))
                    if cur_x == math.floor(x_end):
                        x_multiplier -= (math.ceil(x_end) - x_end)
                    # find the y_multiplier
                    y_multiplier = 1
                    if cur_y == math.floor(y_start):
                        y_multiplier -= (y_start - math.floor(y_start))
                    if cur_y == math.floor(y_end):
                        y_multiplier -= (math.ceil(y_end) - y_end)
                    sum += x_multiplier * y_multiplier * get_pixel(image, cur_x, cur_y)
                    cur_y += 1
                cur_x += 1
            weighted_sum = sum / ((x_end - x_start) * (y_end - y_start))
            result['pixels'].append(weighted_sum)
    # Make sure it is a valid image
    return round_and_clip_image(result)

    # COLOR FILTERS

"""
If color = 0, convert the red pixels to a grayscale image
If color = 1, convert the green pixels to a grayscale image
If color = 2, convert the blue pixels to a grayscale image
"""


def gray_image_from_color_image(image, color):
    result = {
        'width': image['width'],
        'height': image['height'],
        'pixels': [pixel[color] for pixel in image['pixels']],
    }
    return result


"""
Combines the three grayscale images into a colored image according to color
"""


def color_image_from_gray_images(image_red, image_green, image_blue):
    result = {
        'width': image_red['width'],
        'height': image_red['height'],
        'pixels': [rgb_tuple for rgb_tuple in zip(image_red['pixels'], image_green['pixels'], image_blue['pixels'])],
    }
    return result


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """

    def filter_image(im):
        red_image = gray_image_from_color_image(im, 0)
        green_image = gray_image_from_color_image(im, 1)
        blue_image = gray_image_from_color_image(im, 2)
        new_red_image = filt(red_image)
        new_green_image = filt(green_image)
        new_blue_image = filt(blue_image)
        return color_image_from_gray_images(new_red_image, new_green_image, new_blue_image)

    return filter_image

# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    filename = "output/" + filename
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    print("In order to run, put the image into the input folder and change the names.")
    size = (300, 800)
    im = load_color_image("input/frog.png")
    save_color_image(color_filter_from_greyscale_filter(resized(size))(im), "resized.png")
