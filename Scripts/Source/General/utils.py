import struct


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
