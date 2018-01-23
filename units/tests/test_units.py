from __future__ import division, absolute_import, print_function
from units import *

# add openrocketengine to env. variables so we can import openrocketengine here
def test_Value():
    thing = Value(100,'kg')

class TestImperial(object):
    def test_add(self):
        a = Value(1, ['m','s'])
        b = Value(2, ['m','s'])
        
