#!/usr/bin/env python3

import awsgi
from flask import Flask, render_template
import os
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

vehicle = {'vin': None, 'make': None, 'manufacturer': None, 'model': None, 'year': None, 'series': None}

def go():

    found = False
    vin = None
    while found == False:
        vehicle.clear()
        vin = get_random_vin()

        # get year
        if vin[6].isdigit(): # check if vehicle is pre 2010
            year = years_before_2010[vin[9]] 
        else:
            year = years_after_2010[vin[9]] 
            
        # check if vin is valid
        r = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/' + vin + '?format=json&modelyear=' + str(year))
        json = r.json()
        if found == False:
            for r in json['Results']:
                    # check error code value
                    if r['VariableId'] == 143:
                        if r['Value'] == '0':
                            vehicle['vin'] = vin
                            found = True
                        else:
                            break

                    # make
                    if r['VariableId'] == 26:
                        vehicle['make'] = r['Value'].title()

                    # model
                    if r['VariableId'] == 28:
                        vehicle['model'] = r['Value'].title()

                    # year
                    if r['VariableId'] == 29:
                        vehicle['year'] = r['Value']


    qr_code = pyqrcode.create(vin)
    qr_code.png('static/vin_qr_code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])
    
    return vehicle



app = Flask(__name__)
@app.route("/")
def home():
    data = go()
    return render_template("index.html", data=data)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(debug=True)

#def lambda_handler(event, context):
#    return awsgi.response(app, event, context)

