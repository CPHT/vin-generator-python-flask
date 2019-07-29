#!/usr/bin/env python3

import pprint
import requests

pp = pprint.PrettyPrinter()

vin = '1GNFK13087R286019'



#GetAllManufacturers?format=json'

#r = requests.get(url)
#json = r.json()
#results = json['Results']
#for result in results:
    #print (result['Mfr_CommonName'])

class Manufacturer(object):

    def __init__(self, json_text):
        if json_text:
            self.country        = json_text.get('Country', None)
            self.common_name    = json_text.get('Mfr_CommonName', None)
            self.id             = json_text.get('Mfr_ID', None)
            self.name           = json_text.get('Mfr_Name', None)
            self.vehicle_types  = json_text.get('VehicleTypes', None)

    def __repr__(self):
        return self.name

    def url_friendly_name(self):
        rv = self.name.replace(' ', '%20')
        rv = rv.replace('.', '')
        return rv


def make_request(path):
    try:
        r = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/' + path + '?format=json')
    except Exception as e:
        return e
    json = r.json()
    return json['Results']

def get_all_manufacturers():
    manufacturers = []
    r = make_request('GetAllManufacturers')
    for m in r:
        manufacturers.append(Manufacturer(m))
    return manufacturers

def get_manufacturer_details(manufacturer):
    return make_request('GetManufacturerDetails/' + manufacturer)

def get_wmis_for_manufacturer(manufacturer_short):
    return make_request('GetWMIsForManufacturer/' + manufacturer_short)
    


manufacturers = get_all_manufacturers()
#for m in manufacturers:
#    print (m.url_friendly_name())
print(manufacturers[0].url_friendly_name())
print(get_wmis_for_manufacturer(manufacturers[0].url_friendly_name()))

