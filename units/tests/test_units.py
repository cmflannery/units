from __future__ import division, absolute_import, print_function
from units import *
import pytest

# add openrocketengine to env. variables so we can import openrocketengine here
# def test_Value():
#     thing = Value(100,'kg')

class TestOperations(object):
    def test_basic_SI(self):
        a = Value(1, ['m','s^-1'])
        b = Value(2, ['m','s^-1'])
        c = 2
        # Addition
        assert (a+b).SIValue == (1+2)
        assert (a+b).SIUnits == ['m','s^-1']
        # Subration
        assert (b-a).SIValue == (2-1)
        assert (b-a).SIUnits == ['m','s^-1']
        # Value multiplication
        assert (a*b).SIValue == (1*2)
        assert (a*b).SIUnits == ['m^2','s^-2']
        # Scalar multiplication
        assert (a*c).SIValue == (1*2)
        assert (a*c).SIUnits == ['m','s^-1']
        # Right scalar multiplication
        assert (c*a).SIValue == (2*1)
        assert (c*a).SIUnits == ['m','s^-1']
        # Value division
        assert (a/b).SIValue == (1/2)
        assert (a/b).SIUnits == []
        # Scalar division
        assert (a/c).SIValue == (1/2)
        assert (a/c).SIUnits == ['m','s^-1']
        # Right scalar division
        # assert (c/a).SIValue == (2/1)
        # assert (c/a).SIUnits == ['m^-1','s']
        # Exponent
        assert (b**c).SIValue == (2**2)
        assert (b**c).SIUnits == ['m^2','s^-2']
        # Exponent with decimal fraction
        assert (b**(0.5)).SIValue == (2**(0.5))
        assert (b**(0.5)).SIUnits == ['m^0.5','s^-0.5']
        # Exponent with fraction
        assert (b**(1/2)).SIValue == (2**(1/2))
        assert (b**(1/2)).SIUnits == ['m^0.5','s^-0.5']

    def test_basic_IM(self):
        a = Value(1, ['ft','s^-1'])
        b = Value(2, ['ft','s^-1'])
        c = 2
        # Addition
        assert abs((a+b).IMValue - (1+2)) < 1e-4
        assert (a+b).IMUnits == ['ft','s^-1']
        # Subration
        assert abs((b-a).IMValue - (2-1)) < 1e-4
        assert (b-a).IMUnits == ['ft','s^-1']
        # Value multiplication
        assert abs((a*b).IMValue - (1*2)) < 1e-4
        assert (a*b).IMUnits == ['ft^2','s^-2']
        # Scalar multiplication
        assert abs((a*c).IMValue - (1*2)) < 1e-4
        assert (a*c).IMUnits == ['ft','s^-1']
        # Right scalar multiplication
        assert abs((c*a).IMValue - (2*1)) < 1e-4
        assert (c*a).IMUnits == ['ft','s^-1']
        # Value division
        assert abs((a/b).IMValue - (1/2)) < 1e-4
        assert (a/b).IMUnits == []
        # Scalar division
        assert abs((a/c).IMValue - (1/2)) < 1e-4
        assert (a/c).IMUnits == ['ft','s^-1']
        # Right scalar division
        # assert abs((c/a).IMValue - (2/1)) < 1e-4
        # assert (c/a).IMUnits == ['ft^-1','s']
        # Exponent
        assert abs((b**c).IMValue - (2**2)) < 1e-4
        assert (b**c).IMUnits == ['ft^2','s^-2']
        # Exponent with decimal fraction
        assert abs((b**0.5).IMValue - (2**0.5)) < 1e-4
        assert (b**(0.5)).IMUnits == ['ft^0.5','s^-0.5']
        # Exponent with fraction
        assert abs((b**(1/2)).IMValue - (2**(1/2))) < 1e-4
        assert (b**(1/2)).IMUnits == ['ft^0.5','s^-0.5']

    def test_logic(self):
        a = Value(1, ['m','s^-1'])
        b = Value(2, ['m','s^-1'])
        assert (a<b) == True
        assert (a<a) == False
        assert (a<=b) == True
        assert (a<=a) == True
        assert (a==b) == False
        assert (a==a) == True
        assert (a!=b) == True
        assert (a!=a) == False
        assert (a>=b) == False
        assert (a>=a) == True
        assert (a>b) == False
        assert (a>a) == False

    def test_expectedTypeError(self):
        a = Value(1, ['m','s^-1'])
        b = Value(2, ['m','s^-1'])
        c = 2
        d = '2'
        # Basic Operations
        with pytest.raises(TypeError):
            a+c
        with pytest.raises(TypeError):
            a-c
        with pytest.raises(TypeError):
            a*d
        with pytest.raises(TypeError):
            d*a
        with pytest.raises(TypeError):
            a/d
        with pytest.raises(TypeError):
            a**b
        with pytest.raises(TypeError):
            a**d
        # Logic operations
        with pytest.raises(TypeError):
            a<c
        with pytest.raises(TypeError):
            a<=c
        with pytest.raises(TypeError):
            a==c
        with pytest.raises(TypeError):
            a!=c
        with pytest.raises(TypeError):
            a>=c
        with pytest.raises(TypeError):
            a>c

    def test_expectedDimsDoNotAgreeError(self):
        a = Value(1, ['m','s^-1'])
        b = Value(2, ['m','s'])
        # Basic Operations
        with pytest.raises(DimsDoNotAgreeError):
            a+b
        with pytest.raises(DimsDoNotAgreeError):
            a-b
        # Logic operations
        with pytest.raises(DimsDoNotAgreeError):
            a<b
        with pytest.raises(DimsDoNotAgreeError):
            a<=b
        with pytest.raises(DimsDoNotAgreeError):
            a==b
        with pytest.raises(DimsDoNotAgreeError):
            a!=b
        with pytest.raises(DimsDoNotAgreeError):
            a>=b
        with pytest.raises(DimsDoNotAgreeError):
            a>b
