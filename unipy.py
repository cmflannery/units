from __future__ import print_function, division, absolute_import
import numpy as numpy


class value(object):
    def __init__(self, value, units):
        """
        Units expected as follows:
            ['in', 's^-2']
        I.e. all values in numerator with positive and negative
        exponents indicated with a carrot.
        """
        self.value = float(value)
        self.units = units
        self.convert()

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    def __call__(self):
        return self
    
    def __add__(self,b):
        if b.SIUnits != self.SIUnits:
            print('Error: Dimensions do not agree.')
        return value(self.SIValue+b.SIValue, self.SIUnits)

    def __sub__(self,b):
        if type(b) != value:
            raise TypeError('Subtraction not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(value)})
        if b.SIUnits != self.SIUnits:
            print('Error: Dimensions do not agree.')
        return value(self.SIValue-b.SIValue, self.SIUnits)

    @property
    def SIValue(self):
        factor = 1
        for element in self.units:
            try:
                things = element.split('^')
                exponent = float(things[1])
                if exponent == int(exponent):
                    exponent = int(exponent)
                unit = things[0]
            except IndexError:
                exponent = 1
                unit = element
            conversion = self.conversion_factors[unit]
            factor *= conversion**exponent
        return self.value * factor

    @property
    def SIUnits(self):
        self.__SIUnits = []
        for element in self.units:
            try:
                things = element.split('^')
                exponent = float(things[1])
                if exponent == int(exponent):
                    exponent = int(exponent)
                unit = self.conversion_units[things[0]]
                self.__SIUnits.append(str(unit)+'^'+str(exponent))
            except IndexError:
                exponent = 1
                unit = self.conversion_units[element]
                self.__SIUnits.append(str(unit))
        return self.__SIUnits

    @property
    def SI(self):
        return [self.SIValue, self.SIUnits]

    def convert(self):
        self.conversion_units = {
            'm': 'm',
            'km': 'm',
            'in': 'm',
            'ft': 'm',
            'yd': 'm',
            'mi': 'm',
            's': 's',
            'min': 's',
            'h': 's'
        }
        self.conversion_factors = {
            'm': 1.0,
            'km': 0.001,
            'in': 0.254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.34,
            's': 1,
            'min': 60,
            'h': 3600,
            'N':1
        }


class array(object):
    def __init__(self, values, units):
        pass


def test():
    a = value('100', ['mi','h^-1'])
    b = value('10', ['m','s^-1'])
    c = value('90', ['m','s^-2'])


    print('a', a.SI)
    print('b', b.SI)
    print('addition', (a+b).SI)
    print('subtraction', (a-b).SI)

    a-10

if __name__ == '__main__':
    test()