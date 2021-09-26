from math import radians, cos, sin, asin, sqrt, floor, pow, atan2, degrees
import math


lat1 = 11.00461011    
lon1 = 76.95691543
lat2 = 11.0070471
lon2 = 76.96110704
dLon = radians(lon2 - lon1)
lat1 = radians(lat1);
lat2 = radians(lat2);
lon1 = radians(lon1);

Bx = cos(lat2) * cos(dLon);
By = cos(lat2) * sin(dLon);
lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1) + Bx) * (cos(lat1) + Bx) + By * By));
lon3 = lon1 + atan2(By, cos(lat1) + Bx);
lat3 = degrees(lat3)
lon3 = degrees(lon3)

print(lat1, lon1, lat2, lon2, lat3, lon3)