from h3 import h3
from math import radians, cos, sin, asin, sqrt , floor, pow
import numpy as np
import math
import csv
from folium import folium
from folium import features
from folium import map

print('ifd')
n = 0
while n < 21 :
	print('n=',n,'ifd=', 0.152 * pow(2,n))
	n += 1

print('edge length')	
res = 0
while res < 16 :
	print('res=', res, 'edge length=', h3.edge_length(res, unit='km'), 'km')
	res += 1
	
