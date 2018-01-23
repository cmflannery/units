""" units.py provides unit conversion and handling functionality for
scientific python applications """
from __future__ import print_function, division, absolute_import


class Value(object):
    def __init__(self, value, units):
        """
        Units expected as follows:
            ['in', 's^-2']
        I.e. all values in numerator with positive and negative
        exponents indicated with a carrot.
        """
        self.__value = float(value)
        if type(units) != list:
            units = [units]
        self.__units = units
        self.convert()

    @property
    def value(self):
        return self.__value

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    def __call__(self):
        return self

    def __add__(self,b):
        if type(b) != Value:
            raise TypeError('Addition not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('Addition not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return Value(self.SIValue+b.SIValue, self.SIUnits)

    def __sub__(self,b):
        if type(b) != Value:
            raise TypeError('Subtraction not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('Subtraction not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return Value(self.SIValue-b.SIValue, self.SIUnits)

    def __mul__(self,b):
        if (type(b) != Value) and type(b) != int and type(b) != float:
            raise TypeError('Multiplication not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if type(b) == Value:
            units = self.SIUnits + b.SIUnits
            return Value(self.SIValue*b.SIValue, self.unit_reducer(units))
        else:
            return Value(self.SIValue*b, self.SIUnits)


    def __truediv__(self,b):
        if (type(b) != Value) and type(b) != int and type(b) != float:
            raise TypeError('Division not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if type(b) == Value:
            units = self.SIUnits + self.unit_inverter(b.SIUnits)
            return Value(self.SIValue/b.SIValue, self.unit_reducer(units))
        else:
            return Value(self.SIValue/b, self.SIUnits)

    def __pow__(self,b):
        if (type(b) != int) and (type(b) != float):
            raise TypeError('Power operation not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        return Value(self.SIValue**b, self.units_pow(self.SIUnits, b))

    def __abs__(self):
        return Value(abs(self.SIValue), self.SIUnits)

    def units_pow(self, units, power):
        powed_units = []
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                exponent = float(things[1]) * power
            except IndexError:
                unit = element
                exponent = 1 * power
            powed_units.append(unit + '^' + str(exponent))
        return powed_units

    def unit_inverter(self, units):
        inverted_units = []
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                exponent = -float(things[1])
            except IndexError:
                unit = element
                exponent = -1
            inverted_units.append(unit + '^' + str(exponent))
        return inverted_units

    def unit_reducer(self, units):
        unit_dict = {}
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                exponent = float(things[1])
            except IndexError:
                unit = element
                exponent = 1
            try:
                unit_dict[unit] += exponent
            except KeyError:
                unit_dict[unit] = exponent
        reduced_units = []
        for thing in unit_dict:
            unit = thing + '^' + str(unit_dict[thing])
            reduced_units.append(unit)
        reduced_units = self.remove_zero_units(reduced_units)
        return reduced_units

    def remove_zero_units(self, units):
        removed_units = []
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                exponent = float(things[1])
            except IndexError:
                unit = element
                exponent = 1
            if exponent != 0:
                removed_units.append(unit + '^' + str(exponent))
        return removed_units


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
        return self.__value * factor

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

    @property
    def IMValue(self):
        factor = 1
        for element in self.SIUnits:
            try:
                things = element.split('^')
                exponent = float(things[1])
                if exponent == int(exponent):
                    exponent = int(exponent)
                unit = things[0]
            except IndexError:
                exponent = 1
                unit = element
            conversion = self.conversion_factors_IM[unit]
            factor *= conversion**exponent
        return self.SIValue * factor

    @property
    def IMUnits(self):
        self.__IMUnits = []
        for element in self.SIUnits:
            try:
                things = element.split('^')
                exponent = float(things[1])
                if exponent == int(exponent):
                    exponent = int(exponent)
                unit = self.conversion_units_IM[things[0]]
                self.__IMUnits.append(str(unit)+'^'+str(exponent))
            except IndexError:
                exponent = 1
                unit = self.conversion_units_IM[element]
                self.__IMUnits.append(str(unit))
        return self.__IMUnits

    @property
    def IM(self):
        return [self.IMValue, self.IMUnits]

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
            'h': 's',
            'N': 'N'
        }
        self.conversion_factors = {
            'm': 1.0,
            'km': 1000,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.34,
            's': 1,
            'min': 60,
            'h': 3600,
            'N':1
        }
        self.conversion_units_IM = {
            'm': 'ft',
            's': 's',
            'N': 'lbf'
        }
        self.conversion_factors_IM = {
            'm': 3.2808,
            's': 1,
            'N': 0.22481
        }


class array(object):
    def __init__(self, values, units):
        pass


class DimsDoNotAgreeError(Exception):
    """Exception raised for errors in the input when addition and subration
    units are not in agreement.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        Exception.__init__(self, message)


def test():
    a = Value('100', ['mi','h^-1'])
    b = Value('10', ['m','s^-1'])
    c = Value('90', ['m','s^-2'])
    d = 2
    e = Value('-100', ['m','s^-2'])

    print('a', a.SI)
    print('b', b.SI)
    print('addition', (a+b).SI)
    print('subtraction', (a-b).SI)
    print('multiplication', (a*b).SI)
    print('multiplication', (a*d).SI)
    print('division', (a/b).SI)
    print('division', (a/d).SI)
    print('power', (a**d).SI)
    print('abs', (abs(e)).SI)

    # Error cases
    # print('c+b', (c+b).SI) # raises DimsDoNotAgreeError
    # a-10

if __name__ == '__main__':
    test()
