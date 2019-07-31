#!/usr/bin/env python3

from libvin.decoding import Vin
from libvin.static import WMI_MAP
import pyqrcode
import random
import requests
from include import *

def get_random_vin():
    first_8 = random.choice(list(vin_prefixes))
    first_10 = first_8 + 'A' + vin_prefixes[first_8] # 'A' is a temporary placeholder for the checksum char
    last_7 = ''.join([random.choice(base_vin_map) for n in range(7)])

    vin = first_10 + last_7
    vin = vin[:8] + get_check_digit(vin) + vin[9:] # replace checksum digit with valid value
    return vin


def get_check_digit(vin):
    ii = 0
    product_sum = 0
    for c in vin:
        if ii == 8:
            value = 0
        elif c.isdigit():
            value = int(c)
        else:
            value = int(check_digit_values[c])
        weight = check_digit_weights[ii]
        product = value * weight
        product_sum += product
        ii += 1

    remainder = product_sum % 11
    if remainder == 10:
        return 'X'
    else:
        return str(remainder)


found = False
vin = None
while found == False:
    vin = get_random_vin()

    # get year
    if vin[6].isdigit(): # check if vehicle is pre 2010
        year = years_before_2010[vin[9]] 
    else:
        year = years_after_2010[vin[9]] 
        
    # check if vin is valid
    r = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/' + vin + '?format=json&modelyear=' + str(year))
    json = r.json()
    for r in json['Results']:
        if found == False:
            # check error code value
            if r['VariableId'] == 143:
                if r['Value'] == '0':
                    print (vin)
                    found = True
                    break

qr_code = pyqrcode.create(vin)
qr_code.png('qr_code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
qr_code.show()

