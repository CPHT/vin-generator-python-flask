#!/usr/bin/env python3

from libvin.decoding import Vin
from libvin.static import WMI_MAP
import random
import requests
from include import *

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
    first_8 = random.choice(list(vin_prefixes))
    first_10 = first_8 + 'A' + vin_prefixes[first_8]
    last_7 = ''.join([random.choice(base_vin_map) for n in range(7)])

    vin = first_10 + last_7
    vin = vin[:8] + get_check_digit(vin) + vin[9:]
    return vin


def get_check_digit(vin):
    ii = 0
    product_sum = 0
    for c in vin:
        if ii != 9:
            if c.isdigit():
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
while found == False:
    vin = get_random_vin()

    # get year
    if vin[6].isdigit(): # check if vehicle is pre 2010
        year = years_before_2010[vin[9]] 
    else:
        year = years_after_2010[vin[9]] 
        
    r = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/' + vin + '?format=json&modelyear=' + str(year))
    json = r.json()
    for r in json['Results']:
        if r['VariableId'] == 143:
            if r['Value'] == '0':
                print ("VALID", vin)
                found = True
                break



