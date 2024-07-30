import struct

import glm
import numpy as np
import pygame as pg


class IndexableProperty:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

    def __getitem__(self, key):
        if hasattr(self.fget, '__getitem__'):
            return self.fget(self.obj)[key]
        raise TypeError("'{}' object is not subscriptable".format(type(self.fget).__name__))

    def __setitem__(self, key, value):
        if hasattr(self.fset, '__setitem__'):
            self.fset(self.obj, key, value)
        else:
            raise TypeError("'{}' object does not support item assignment".format(type(self.fset).__name__))

    def __delitem__(self, key):
        if hasattr(self.fdel, '__delitem__'):
            self.fdel(self.obj, key)
        else:
            raise TypeError("'{}' object does not support item deletion".format(type(self.fdel).__name__))


def bytes_to_normalized_tuple(byte_data):
    '''
    convert from hex to normalized color system(0.0 — 1.0)
    :param byte_data: hex color
    :return: normalized color tuple
    '''
    # Unpack the byte data into integers
    int_values = struct.unpack('BBB', byte_data)
    # Normalize the values to the range [0, 1]
    normalized_values = tuple(value / 255.0 for value in int_values)
    return normalized_values


def get_data_elements_by_indices(vertices, indices) -> np.ndarray:
    '''
    :param vertices: list data for all vertices
    :param indices: list index tuple with sequence vertices data
    :return: one-dimension sequence vertex data based on indices
    '''
    data = [vertices[ind] for triangle in indices for ind in triangle]
    return np.array(data, dtype='f4')


def calculate_width_letters(path):
    '''
    Calculate width of letters in text-tail texture 512 by 512.
    :param path: path to image
    :return: one dimensional list with relative (0.0—1.0) width letter
    '''
    # Load the image
    img = pg.image.load(path)
    width, height = img.get_size()

    num_letters_per_row = 16  # Adjust this based on your texture layout
    num_letters_per_col = 16  # Adjust this based on your texture layout

    letter_width = width // num_letters_per_row
    letter_height = height // num_letters_per_col

    letter_widths = []

    for row in range(num_letters_per_col):
        for col in range(num_letters_per_row):
            max_right_white_pixel = 0
            for y in range(row * letter_height, (row + 1) * letter_height):
                for x in range(col * letter_width, (col + 1) * letter_width):
                    r, g, b, a = img.get_at((x, y))
                    if a != 0:  # White pixel
                        max_right_white_pixel = max(max_right_white_pixel, x)

            # Calculate the real width of the letter
            real_width = max(0, (max_right_white_pixel - col * letter_width)) / letter_width
            letter_widths.append(real_width)

    letter_widths[16 * 2 + 0] = 0.5

    return letter_widths


def rainbow_color(t):
    """
    Returns an RGB color representing a rainbow shimmering effect based on the time in seconds.

    Parameters:
    t (float): Time in seconds.

    Returns:
    tuple: RGB color as a tuple of three floats in the range [0, 1].
    """
    # Normalize time to a value between 0 and 1
    hue = (t % 6) / 6

    # Convert hue to RGB
    r = max(0, min(1, abs(hue * 6 - 3) - 1))
    g = max(0, min(1, 2 - abs(hue * 6 - 2)))
    b = max(0, min(1, 2 - abs(hue * 6 - 4)))

    return glm.vec4(r, g, b, 1)
