#!/usr/bin/env python3

from libvin.decoding import Vin
from libvin.static import WMI_MAP
import random
import requests
from prefixes import vin_prefixes


def get_random_vin():
    base_vin_map = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    vds_4_through_8 = ''.join([random.choice(base_vin_map) for n in range(5)])
    vds_9 = 'A'

    first_8 = random.choice(list(vin_prefixes))
    first_10 = first_8 + 'A' + vin_prefixes[first_8]
    last_7 = ''.join([random.choice(base_vin_map) for n in range(7)])

    vin = first_10 + last_7
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



