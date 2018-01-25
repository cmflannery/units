from __future__ import division, absolute_import, print_function
from units import *
import pytest

# add openrocketengine to env. variables so we can import openrocketengine here
def test_Value():
    thing = Value(100,'kg')

def test_units_sorting():
    a = Value(10, ['s','m^-2','kg^10','ft','h^6','N^-0.01','psi'])
    b = Value(10, ['h^6','N^-0.01','psi','ft','s','m^-2','kg^10'])
    c = Value(10, ['m','s^-2'])
    d = Value(10, ['h^-2','mi'])
    assert a.units == b.units
    assert a.SIUnits == b.SIUnits
    assert a.IMUnits == b.IMUnits
    assert (c*d).SIUnits == ['m^2','s^-4']

class TestOperations(object):
    def test_basic_SI(self):
        a = 1; a_val = Value(a, ['m','s^-1'])
        b = 2; b_val = Value(b, ['m','s^-1'])
        c = 2
        d = 2
        # Negation
        assert (-a_val).SIValue == (-a)
        assert (-a_val).SIUnits == ['m','s^-1']
        # Absolute value
        assert abs(-a_val).SIValue == abs(-a)
        assert abs(-a_val).SIUnits == ['m','s^-1']
        # Addition
        assert (a_val+b_val).SIValue == (a+b)
        assert (a_val+b_val).SIUnits == ['m','s^-1']
        # Subration
        assert (b_val-a_val).SIValue == (b-a)
        assert (b_val-a_val).SIUnits == ['m','s^-1']
        # Value multiplication
        assert (a_val*b_val).SIValue == (a*b)
        assert (a_val*b_val).SIUnits == ['m^2','s^-2']
        # Scalar multiplication
        assert (a_val*c).SIValue == (a*c)
        assert (a_val*c).SIUnits == ['m','s^-1']
        # Right scalar multiplication
        assert (c*a_val).SIValue == (c*a)
        assert (c*a_val).SIUnits == ['m','s^-1']
        # Value division
        assert (a_val/b_val).SIValue == (a/b)
        assert (a_val/b_val).SIUnits == []
        # Scalar division
        assert (a_val/c).SIValue == (a/c)
        assert (a_val/c).SIUnits == ['m','s^-1']
        # Right scalar division
        # assert (c/a_val).SIValue == (c/a)
        # assert (c/a_val).SIUnits == ['m^-1','s']
        # Exponent
        assert (b_val**d).SIValue == (b**d)
        assert (b_val**d).SIUnits == ['m^'+str(d),'s^-'+str(d)]
        # Exponent with decimal fraction
        assert (b_val**(0.5)).SIValue == (b**(0.5))
        assert (b_val**(0.5)).SIUnits == ['m^0.5','s^-0.5']
        # Exponent with fraction
        assert (b_val**(1/2)).SIValue == (b**(1/2))
        assert (b_val**(1/2)).SIUnits == ['m^0.5','s^-0.5']

    def test_basic_IM(self):
        a = 1; a_val = Value(a, ['ft','s^-1'])
        b = 2; b_val = Value(b, ['ft','s^-1'])
        c = 2
        d = 2
        # Addition
        assert abs((a_val+b_val).IMValue - (a+b)) < 1e-4
        assert (a_val+b_val).IMUnits == ['ft','s^-1']
        # Subration
        assert abs((b_val-a_val).IMValue - (b-a)) < 1e-4
        assert (b_val-a_val).IMUnits == ['ft','s^-1']
        # Value multiplication
        assert abs((a_val*b_val).IMValue - (a*b)) < 1e-4
        assert (a_val*b_val).IMUnits == ['ft^2','s^-2']
        # Scalar multiplication
        assert abs((a_val*c).IMValue - (a*c)) < 1e-4
        assert (a_val*c).IMUnits == ['ft','s^-1']
        # Right scalar multiplication
        assert abs((c*a_val).IMValue - (c*a)) < 1e-4
        assert (c*a_val).IMUnits == ['ft','s^-1']
        # Value division
        assert abs((a_val/b_val).IMValue - (a/b)) < 1e-4
        assert (a_val/b_val).IMUnits == []
        # Scalar division
        assert abs((a_val/c).IMValue - (a/c)) < 1e-4
        assert (a_val/c).IMUnits == ['ft','s^-1']
        # Right scalar division
        # assert abs((c/a_val).IMValue - (c/a)) < 1e-4
        # assert (c/a_val).IMUnits == ['ft^-1','s']
        # Exponent
        assert abs((b_val**d).IMValue - (b**d)) < 1e-4
        assert (b_val**d).IMUnits == ['ft^'+str(d),'s^-'+str(d)]
        # Exponent with decimal fraction
        assert abs((b_val**0.5).IMValue - (b**0.5)) < 1e-4
        assert (b_val**(0.5)).IMUnits == ['ft^0.5','s^-0.5']
        # Exponent with fraction
        assert abs((b_val**(1/2)).IMValue - (b**(1/2))) < 1e-4
        assert (b_val**(1/2)).IMUnits == ['ft^0.5','s^-0.5']

    def test_logic(self):
        a = 1; a_val = Value(a, ['m','s^-1'])
        b = 2; b_val = Value(b, ['m','s^-1'])
        assert (a_val<b_val) == (a<b)
        assert (a_val<a_val) == (a<a)
        assert (a_val<=b_val) == (a<=b)
        assert (a_val<=a_val) == (a<=a)
        assert (a_val==b_val) == (a==b)
        assert (a_val==a_val) == (a==a)
        assert (a_val!=b_val) == (a!=b)
        assert (a_val!=a_val) == (a!=a)
        assert (a_val>=b_val) == (a>=b)
        assert (a_val>=a_val) == (a>=a)
        assert (a_val>b_val) == (a>b)
        assert (a_val>a_val) == (a>a)

class TestExpectedErrors(object):
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
