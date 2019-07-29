#!/usr/bin/env python3

import vinlib



# generate random vin
#Y=2000, 1='01, 2='02, 3='03, 4='04, 5='05, 6='06, 7='07, 8='08, 9='09, A='10, B='11, C='12, D='13, E='14, F='15, G='16, H='17, J='18, K='19, L='20.


vin = '1GNFK13087R286019'
print (vinlib.Vin(vin).check)

wmi = vin[:3]
vds = vin[3:9]
vis = vin[9:]

lookup = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'] 

regions = {'Africa': ['A', 'B', 'C'], 'North America': ['1', '2', '3', '4', '5'], 'South America': ['8', '9'], 'Asia': ['J', 'K', 'L', 'M', 'N', 'P', 'R'], 'Europe': ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 'Oceania': ['6']}

#country = {


#for l in lookup:

    #for region in regions:
    ##    if wmi[0] in regions[region]:
        #if l in regions[region]:
            #print (l, region)


#print (vin)
#print (wmi)
#print (vds)
#print (vis)





