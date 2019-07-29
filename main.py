#!/usr/bin/env python3

from libvin.decoding import Vin
from libvin.static import WMI_MAP
import random

vin = '1GNFK13087R286019'

v = Vin(vin)
print (v.region)
print (v.country)
print (v.make)
print (v.manufacturer)
print (v.vds)
print (v.vis)
print (v.vsn)
print (v.wmi)
print (v.year)

def get_random_vin():
    key = random.choice(list(WMI_MAP))
    wmi = key
    print (key, WMI_MAP[key])


get_random_vin()


# if vin.is_valid()
