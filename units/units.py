""" units.py provides unit conversion and handling functionality for
scientific python applications """
from __future__ import print_function, division, absolute_import
import numpy as np


class Value(object):
    def __init__(self, value, units):
        """
        Units expected as follows:
            ['in', 's^-2']
        I.e. all values in numerator with positive and negative
        exponents indicated with a carrot.
        """
        self.conversions()
        self.__value = float(value)
        if type(units) != list:
            units = [units]
        self.__units = self.units_sorted(units)

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
        if type(b) != Value and type(b) != int and type(b) != np.float32 and type(b) != np.float64:
            raise TypeError('Multiplication not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if type(b) == Value:
            units = self.SIUnits + b.SIUnits
            return Value(self.SIValue*b.SIValue, self.units_simplify(units))
        else:
            return Value(self.SIValue*b, self.SIUnits)

    def __rmul__(self,b):
        return self.__mul__(b)

    def __truediv__(self,b):
        if type(b) != Value and type(b) != int and type(b) != np.float32 and type(b) != np.float64:
            raise TypeError('Division not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if type(b) == Value:
            units = self.SIUnits + self.units_inverter(b.SIUnits)
            return Value(self.SIValue/b.SIValue, self.units_simplify(units))
        else:
            return Value(self.SIValue/b, self.SIUnits)

    def __pow__(self,b):
        if type(b) != int and type(b) != float and type(b) != np.float32 and type(b) != np.float64:
            raise TypeError('Power operation not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        return Value(self.SIValue**b, self.units_pow(self.SIUnits, b))

    def __neg__(self):
        return Value(-(self.SIValue), self.SIUnits)

    def __abs__(self):
        return Value(abs(self.SIValue), self.SIUnits)

    def __lt__(self,b):
        if type(b) != Value:
            raise TypeError('< not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('< not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue < b.SIValue)

    def __le__(self,b):
        if type(b) != Value:
            raise TypeError('<= not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('<= not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue <= b.SIValue)

    def __eq__(self,b):
        if type(b) != Value:
            raise TypeError('== not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('== not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue == b.SIValue)

    def __ne__(self,b):
        if type(b) != Value:
            raise TypeError('!= not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('!= not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue != b.SIValue)

    def __ge__(self,b):
        if type(b) != Value:
            raise TypeError('>= not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('>= not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue >= b.SIValue)

    def __gt__(self,b):
        if type(b) != Value:
            raise TypeError('> not supported for types %(1)s, %(2)s' % {'1': type(b), '2': type(Value)})
        if b.SIUnits != self.SIUnits:
            raise DimsDoNotAgreeError('> not supported for units %(1)s, %(2)s' % {'1': b.SIUnits, '2': self.SIUnits})
        return (self.SIValue > b.SIValue)

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

    def units_inverter(self, units):
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

    def units_simplify(self, units):
        unit_dict = {}
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                try:
                    exponent = float(things[1])
                except ValueError: # Catch fractional inputs like m^1/2
                    things2 = things[1].split('/')
                    exponent = float(things2[0])/float(things2[1])
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
        reduced_units = self.units_simplify_power(reduced_units)
        return reduced_units

    def units_simplify_power(self, units):
        removed_units = []
        for element in units:
            things = element.split('^')
            try:
                unit = things[0]
                exponent = float(things[1])
            except IndexError:
                unit = element
                exponent = 1
            if exponent == 1:
                removed_units.append(unit)
            elif exponent != 0:
                removed_units.append(unit + '^' + str(exponent))
        return removed_units

    def units_sorted(self, units):
        simplified_units = self.units_simplify(units)
        sorted_units = sorted(simplified_units, key=self.units_sorted_key)
        return sorted_units

    def units_sorted_key(self, unit):
        try:
            things = unit.split('^')
            unit = things[0]
        except IndexError:
            pass
        comp = self.comparision_dict[unit]
        return comp

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
            conversion = self.conversion_factors_IM[unit]
            factor *= conversion**exponent
        return self.__value * factor

    @property
    def IMUnits(self):
        self.__IMUnits = []
        for element in self.units:
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

    def conversions(self):
        self.conversion_units = {
            'kg': 'kg',
            'g': 'kg',
            'lbm': 'kg',
            'slug': 'kg',
            'm': 'm',
            'km': 'm',
            'in': 'm',
            'ft': 'm',
            'yd': 'm',
            'mi': 'm',
            's': 's',
            'min': 's',
            'h': 's',
            'N': 'N',
            'lbf': 'N',
            'Pa': 'Pa',
            'psi': 'Pa'
        }
        self.conversion_factors = {
            'kg': 1.0,
            'g': 0.001,
            'lbm': 0.4536,
            'slug': 14.5939,
            'm': 1.0,
            'km': 1000,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.3440,
            's': 1.0,
            'min': 60,
            'h': 3600,
            'N': 1.0,
            'lbf': 4.4482,
            'Pa': 1.0,
            'psi': 6894.7573
        }
        self.conversion_units_IM = {
            'kg': 'lbm',
            'g': 'lbm',
            'lbm': 'lbm',
            'slug': 'lbm',
            'm': 'ft',
            'km': 'ft',
            'in': 'ft',
            'ft': 'ft',
            'yd': 'ft',
            'mi': 'ft',
            's': 's',
            'min': 's',
            'h': 's',
            'N': 'lbf',
            'lbf': 'lbf',
            'Pa': 'psi',
            'psi': 'psi'
        }
        self.conversion_factors_IM = {
            'kg': 2.2046,
            'g': 0.002205,
            'lbm': 1.0,
            'slug': 32.1740,
            'm': 3.2808,
            'km': 3280.8399,
            'in': 1/12,
            'ft': 1.0,
            'yd': 3.0,
            'mi': 5280.0,
            's': 1.0,
            'min': 60,
            'h': 3600,
            'N': 0.2248,
            'lbf': 1.0,
            'Pa': 0.0001450,
            'psi': 1.0
        }
        self.comparision_dict = {
            'kg': 0,
            'g': 1,
            'lbm': 2,
            'slug': 3,
            'm': 4,
            'km': 5,
            'in': 6,
            'ft': 7,
            'yd': 8,
            'mi': 9,
            's': 10,
            'min': 11,
            'h': 12,
            'N': 13,
            'lbf': 14,
            'Pa': 15,
            'psi': 16
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

# def test():
    # a = Value('100', ['mi','h^-1'])
    # b = Value('10', ['m','s^-1'])
    # c = Value('90', ['m','s^-2'])
    # d = 2
    # e = Value('-100', ['m','s^-2'])
    #
    # print('a', a.SI)
    # print('b', b.SI)
    # print('addition', (a+b).SI)
    # print('subtraction', (a-b).SI)
    # print('multiplication', (a*b).SI)
    # print('multiplication', (a*d).SI)
    # print('division', (a/b).SI)
    # print('division', (a/d).SI)
    # print('power', (a**d).SI)
    # print('abs', (abs(e)).SI)
    #
    # print('a', a.IM)
    # print('b', b.IM)
    # print('addition', (a+b).IM)
    # print('multiplication', (a*b).IM)
    # print('division', (a/b).IM)


    # Error cases
    # print('c+b', (c+b).SI) # raises DimsDoNotAgreeError
    # a-10

if __name__ == '__main__':
    # test()
    pass
