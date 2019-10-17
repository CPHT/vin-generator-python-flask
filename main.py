#!/usr/bin/env python3

import boto3
from flask import Flask, render_template, request
import os
import pyqrcode
import random
import re
import requests
from include import *

vehicle = {'vin': None, 'make': None, 'manufacturer': None, 'model': None, 'year': None, 'series': None}

def make_random_vin():
    first_8 = random.choice(list(vin_prefixes))
    first_10 = first_8 + 'A' + vin_prefixes[first_8] # 'A' is a temporary placeholder for the checksum char
    last_7 = ''.join([random.choice(base_vin_map) for n in range(7)])

    vin = first_10 + last_7
    vin = vin[:8] + get_check_digit(vin) + vin[9:] # replace checksum digit with valid value
    return vin

def get_random_vin():
    r = requests.get('http://randomvin.com/getvin.php?type=real')
    return r.text

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


def get_vehicle(vin=None):
    manual_entry = False

    if vin != None:
        manual_entry = True

    found = False
    while found == False:
        vehicle.clear()
        if manual_entry == False:
            vin = get_random_vin()
            #vin = make_random_vin()

        # get year
        if vin[6].isdigit(): # check if vehicle is pre 2010
            year = years_before_2010[vin[9]] 
        else:
            year = years_after_2010[vin[9]] 
            
        # check if vin is valid
        try:
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
                                if manual_entry:
                                    return 0
                                break

                        # make
                        if r['VariableId'] == 26:
                            vehicle['make'] = r['Value'].upper()

                        # model
                        if r['VariableId'] == 28:
                            vehicle['model'] = r['Value'].upper()

                        # year
                        if r['VariableId'] == 29:
                            vehicle['year'] = r['Value']
        except Exception as e:
            pass


    # get qr code
    qr_code = pyqrcode.create(vin)
    qr_code.png('/tmp/vin_qr_code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xff])

    # get image
    r = requests.get('http://www.carimagery.com/api.asmx/GetImageUrl?searchTerm=' + vehicle['year'] + '+' + vehicle['make'].partition(' ')[0] + '+' + vehicle['model'].partition(' ')[0])
    vehicle['image'] = re.sub('<[^<]+?>', '', r.text)
    print (vehicle['image'])
    
    return vehicle


app = Flask(__name__, static_folder="/tmp")
@app.route("/")#, methods = ['POST', 'GET'])
def home():
    data = get_vehicle()
    s3 = boto3.client('s3')
    s3.upload_file('/tmp/vin_qr_code.png', 'vin-generator-python-flask', 'static/vin_qr_code.png')
    return render_template("index.html", data=data)

@app.route("/", methods = ['POST'])
def form_post():
    vin = request.form['text']
    if vin:
        data = get_vehicle(vin)
        if data:
            return render_template("index.html", data=data)
    return "Invalid VIN"

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

