from h3 import h3
from math import radians, cos, sin, asin, sqrt , floor, pow
import numpy as np
import math
import csv
from folium import folium
from folium import features
from folium import map

n = 2
edgelength = 0.152 * pow(2,n)
print (edgelength)
radius = floor(edgelength/ (h3.edge_length(0, unit='km') ));
print('0:', radius)
radius = floor(edgelength/ (h3.edge_length(1, unit='km') ));
print('1:', radius)
radius = floor(edgelength/ (h3.edge_length(2, unit='km') ));
print('2:', radius)
radius = floor(edgelength/ (h3.edge_length(3, unit='km') ));
print('3:', radius)
radius = floor(edgelength/ (h3.edge_length(4, unit='km') ));
print('4:', radius)
radius = floor(edgelength/ (h3.edge_length(5, unit='km') ));
print('5:', radius)
radius = floor(edgelength/ (h3.edge_length(6, unit='km') ));
print('6:', radius)
radius = floor(edgelength/ (h3.edge_length(7, unit='km') ));
print('7:', radius)
radius = floor(edgelength/ (h3.edge_length(8, unit='km') ));
print('8:', radius)
radius = floor(edgelength/ (h3.edge_length(9, unit='km') ));
print('9:', radius)
radius = floor(edgelength/ (h3.edge_length(10, unit='km') ));
print('10:', radius)
radius = floor(edgelength/ (h3.edge_length(11, unit='km') ));
print('11:', radius)
radius = floor(edgelength/ (h3.edge_length(12, unit='km') ));
print('12:', radius)
radius = floor(edgelength/ (h3.edge_length(13, unit='km') ));
print('13:', radius)
radius = floor(edgelength/ (h3.edge_length(14, unit='km') ));
print('14:', radius)
radius = floor(edgelength/ (h3.edge_length(15, unit='km') ));
print('15:', radius)

