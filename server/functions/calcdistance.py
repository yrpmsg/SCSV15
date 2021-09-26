from math import radians, cos, sin, asin, sqrt, floor, pow
import math


lat1 = 11.00461011    
lon1 = 76.95691543
lat2 = 11.0070471
lon2 = 76.96110704

lon1 = radians(lon1)     
lon2 = radians(lon2) 
lat1 = radians(lat1) 
lat2 = radians(lat2) 
   
# Haversine formula  
dlon = lon2 - lon1  
dlat = lat2 - lat1 
a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

c = 2 * asin(sqrt(a))  
   
# Radius of earth in kilometers. Use 3956 for miles 
r = 6371
       
# calculate the result 
print(c * r) 
