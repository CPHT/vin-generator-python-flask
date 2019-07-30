#!/usr/bin/env python3

from libvin.decoding import Vin
from libvin.static import WMI_MAP
import random
import requests

#vin = '1GNFK13087R286019'
#vin = '1M8GDM9AAKP042788'

#v = Vin(vin)
#print (v.region)
#print (v.country)
#print (v.make)
#print (v.manufacturer)
#print (v.vds)
#print (v.vis)
#print (v.vsn)
#print (v.wmi)
#print (v.year)


def get_random_vin():
    #wmi = random.choice(list(WMI_MAP))
    wmi = '5J6'

    base_vin_map = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # can not use I, O, Q, U, Z
    year_model_map = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'V', 'W', 'X', 'Y']

    vds_4_through_8 = ''.join([random.choice(base_vin_map) for n in range(5)])
    #TODO this is 0-9 if in NA, else it's X
    # temp
    vds_9 = 'A'

    vis_10 = random.choice(year_model_map)
    vis_11 = random.choice(base_vin_map)
    vis_12_through_17 = ''.join([random.choice(base_vin_map) for n in range(6)])

    vin = wmi + vds_4_through_8 + vds_9 + vis_10 + vis_11 + vis_12_through_17
    vin = vin[:8] + get_check_digit(vin) + vin[9:]
    return vin


def get_check_digit(vin):
    values = {'A': 1, 'B': '2', 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9}

    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

    ii = 0
    product_sum = 0
    for c in vin:
        if ii != 9:
            if c.isdigit():
                value = int(c)
            else:
                value = int(values[c])
            weight = weights[ii]
            product = value * weight
            product_sum += product
            ii += 1

    remainder = product_sum % 11
    if remainder == 10:
        return 'X'
    else:
        return str(remainder)

while True:
    v = Vin(get_random_vin())
    if (v.is_valid):
        print ("VALID", v.vin)
        break



