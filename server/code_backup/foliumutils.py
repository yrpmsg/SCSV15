from h3 import h3
from math import radians, cos, sin, asin, sqrt, floor, pow, atan2, degrees
import numpy as np
import math
import csv
from folium import folium
from folium import features
from folium import map
from ..folium.map import Marker
from ..folium.map import Icon
from ..folium.map import Popup
from ..folium.map import Tooltip
from ..folium.vector_layers import Polygon
from ..folium.vector_layers import PolyLine


def mapit(latitude, longitude, granularity): 
    start_coords = (latitude, longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=granularity, zoom_control=True)
    tooltip = 'Click me!'
    Marker([latitude, longitude], popup='<i>Coimbatore</i>', tooltip=tooltip).add_to(folium_map)
    return folium_map

def plothexagon(latitude, longitude, granularity, hexagons): 
    start_coords = (latitude, longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=granularity, zoom_control=True)
    tooltip = 'Click me!'
    Marker([latitude, longitude], popup='<i>Coimbatore</i>', tooltip=tooltip).add_to(folium_map)
    latitudes=[0, 0, 0, 0, 0, 0]
    longitudes=[0, 0, 0, 0, 0, 0]
    i = 0
    while i < len(hexagons):
        latitudes[i] =hexagons[i][0] 
        longitudes[i] = hexagons[i][1]
        Marker([latitudes[i], longitudes[i]], popup='<i>hexagon point</i>', tooltip=tooltip).add_to(folium_map)
        i += 1
    #Polygon(zip(longitudes, latitudes)).add_to(folium_map)
    Polygon(hexagons).add_to(folium_map)
    return folium_map

def plotkring(latitude, longitude, granularity, hexagons): 
    start_coords = (latitude, longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=granularity, zoom_control=True)
    tooltip = 'Click me!'
    #Marker([latitude, longitude], popup='<i>Coimbatore</i>', tooltip=tooltip).add_to(folium_map)
    latitudes=[]
    longitudes=[]
    i = 0
    while i < len(hexagons):
        latitudes.append(hexagons[i][0])
        longitudes.append(hexagons[i][1])
        Marker([latitudes[i], longitudes[i]], popup='<i>hexagon point</i>', tooltip=tooltip).add_to(folium_map)
        i += 1
    #Polygon(zip(longitudes, latitudes)).add_to(folium_map)
    #Polygon(hexagons).add_to(folium_map)
    return folium_map

def plotgrid(latitude, longitude, granularity, radius, zoomlevel, kring): 
    start_coords = (latitude, longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=zoomlevel, zoom_control=True)
    latitudes=[]
    longitudes=[]
    i = 0
    while i < len(kring):
        latitudes.append(kring[i][0])
        longitudes.append(kring[i][1])
        tooltip = i
        Marker([latitudes[i], longitudes[i]], icon=Icon(color='orange'), popup='<i>DC</i>', tooltip=tooltip).add_to(folium_map)
        i += 1
    h3_address=h3.geo_to_h3(latitude, longitude, granularity)
    kring1=h3.k_ring(h3_address, radius)
    for this_kring in kring1:
        this_hexagon=h3.h3_to_geo_boundary(this_kring)
        #Polygon(zip(longitudes, latitudes)).add_to(folium_map)
        Polygon(this_hexagon).add_to(folium_map)
        j=0
        while j < len(this_hexagon):
            tooltip = j
            Marker([this_hexagon[j][0], this_hexagon[j][1]], icon=Icon(color='green'), popup='<i>Facility</i>', tooltip=tooltip).add_to(folium_map)
            j += 1

    return folium_map

def plotNumberedGridKMNew(latitude, longitude, radius, n, zoomlevel, zlplotlabel, kring):
    """ Determine H3 resolution """
    n_to_granularity=[9,8,8,8,7,6,6,6,5,4,3,3,3,2,1,1,1,0]
    granularity = n_to_granularity[n];
    start_coords = (latitude, longitude)
    
    """ Initialize Map """
    folium_map = folium.Map(location=start_coords, zoom_start=zoomlevel, zoom_control=True)
    latitudes=[]
    longitudes=[]
    DC=[]
    Facility=[]
    
    """ Get Center and K-rings """
    h3_address=h3.geo_to_h3(latitude, longitude, granularity)
    center=h3.h3_to_geo(h3_address)
    centerlat=center[0]
    centerlon=center[1]    
    kring_distances=h3.k_ring_distances(h3_address, radius)
    kring = h3.k_ring(h3_address,radius)
    
    """ Sort K-rings based on bearing """
    i = 0
    thisringSorted=[]
    Sortedarray=[]
    while i < len(kring_distances):
        this_ring_set=kring_distances[i]
        this_ring=list(this_ring_set)    
        j = 0 
        thisring=[]
        while j < len(this_ring):
            geocoord=h3.h3_to_geo(this_ring[j])
            thislatitude=geocoord[0]
            thislongitude=geocoord[1]    
            latitudes.append(thislatitude)
            longitudes.append(thislongitude)
            bearing=np.angle(complex(thislatitude-centerlat,thislongitude-centerlon))*180/math.pi
            if bearing < 0:
                bearing+=360
            #print(i, j, latitudes[j], longitudes[j], bearing)
            thisringpoint=[]
            thisringpoint.append(thislatitude)
            thisringpoint.append(thislongitude)
            thisringpoint.append(bearing)
            thisringpoint.append(i)
            thisring.append(thisringpoint)
            j += 1
        thisringSorted=sorted(thisring, key=lambda x: (x[2]))
        k = 0
        topleft=0
        while k < len(thisringSorted):
            if (thisringSorted[k][2] > 331) & (thisringSorted[k][2] < 332):
                topleft= k
            k += 1
        first=topleft
        last=topleft-1
        j=0
        thisringRolled=[]
        k = first
        while j < len(thisringSorted): 
            thisringRolled.append(thisringSorted[k])
            k += 1
            j += 1
            if k >= len(thisringSorted):
                k = 0 
        Sortedarray.append(thisringRolled)
        i += 1
    i=0
    
    
    
    """ Populate Hexagonal Matrix """
    hexagon=[]
    thisside=[]
    thisring=[]
    thisside.append(center)
    thisring.append(thisside)
    hexagon.append(thisring)
    i = 1
    while i < len(Sortedarray):
        j = 0
        s = 0
        pointsperside = len(Sortedarray[i])/6 
        thisring=[]
        thisside=[]
        while j < len(Sortedarray[i]):
            thisside.append(Sortedarray[i][j])
            s +=1
            if s >= pointsperside:
                thisring.append(thisside)
                thisside=[]
                s = 0
            j +=1
        hexagon.append(thisring)
        thisring=[]
        i+= 1
    
    """ Determine DC and Facility """
    DC_array=[]
    Facilities_array=[]
    Sorted_ring=[]
    
   
    dcnum = 0
    dc_number= 'DC' + str(dcnum).zfill(3) 
    coordinates=[]
    coordinates.append(center[0])
    coordinates.append(center[1])
    thisdc=[]
    thisdc.append(dc_number)
    thisdc.append(coordinates)
    DC_array.append(thisdc)
    dcnum += 1
    tooltip=dc_number
    Marker([center[0], center[1]], icon=Icon(color='orange'), popup='<i>DC</i>', tooltip=tooltip).add_to(folium_map)
    thispoint=[]
    thissortedring=[]
    thispoint.append(tooltip)
    thispoint.append(coordinates)
    thissortedring.append(thispoint)
    Sorted_ring.append(thissortedring)
                
    i = 1
    dcnum = 1
    fcnum = 0
    while i < len(hexagon):
        j=0
        s = 0
        l = 0
        thisring = hexagon[i]
        sidelength = len(hexagon[i][s])
        thisside=hexagon[i][j]
        this ='fc'
        j = i 
        k = 1
        thissortedring=[]
        while l < 6 * sidelength:
            if j >= 6 * sidelength:
                j = 0
            if k >= sidelength:
                k = 0
                s +=1
                if s >= 6:
                    s = 0                
                thisside=hexagon[i][s]
            if (i % 2) == 0: 
                """Alternate between DC and Facility"""
                if this=='dc' :
                    #dc_number= 'DC' + str(dcnum).zfill(3) + 'i' + str(i) + 'j' + str(j)
                    dc_number= 'DC' + str(dcnum).zfill(3) 
                    coordinates=[]
                    coordinates.append(thisside[k][0])
                    coordinates.append(thisside[k][1])
                    thisdc=[]
                    thisdc.append(dc_number)
                    thisdc.append(coordinates)
                    DC_array.append(thisdc)
                    dcnum += 1
                    tooltip=dc_number
                    Marker([thisside[k][0], thisside[k][1]], icon=Icon(color='orange'), popup='<i>DC</i>', tooltip=tooltip).add_to(folium_map)
                    this='fc'
                else:
                    #Facility_Number='FC' + str(fcnum).zfill(4)  + 'i' + str(i) + 'j' + str(j) 
                    Facility_Number='FC' + str(fcnum).zfill(4)  
                    coordinates=[]
                    coordinates.append(thisside[k][0])
                    coordinates.append(thisside[k][1])
                    thisfacility=[]
                    thisfacility.append(Facility_Number)                        
                    thisfacility.append(coordinates)
                    Facilities_array.append(thisfacility)
                    fcnum += 1
                    tooltip=Facility_Number
                    Marker([thisside[k][0], thisside[k][1]], icon=Icon(color='green'), popup='<i>Facility</i>', tooltip=tooltip).add_to(folium_map) 
                    this='dc'
            else:
                #Facility_Number='FC' + str(fcnum).zfill(4)  + 'i' + str(i) + 'j' + str(j)
                Facility_Number='FC' + str(fcnum).zfill(4)  
                coordinates=[]
                coordinates.append(thisside[k][0])
                coordinates.append(thisside[k][1])
                thisfacility=[]
                thisfacility.append(Facility_Number)
                thisfacility.append(coordinates)
                Facilities_array.append(thisfacility)
                fcnum += 1
                tooltip=Facility_Number
                Marker([thisside[k][0], thisside[k][1]], icon=Icon(color='green'), popup='<i>Facility</i>', tooltip=tooltip).add_to(folium_map)
            thispoint=[]
            thispoint.append(tooltip)
            thispoint.append(coordinates)
            thissortedring.append(thispoint)
            thisside[k].append(tooltip)
            k +=1
            j += 1
            l += 1
        Sorted_ring.append(thissortedring)
        i += 1
        

    with open('./public/data/DC.csv', mode='w', newline='') as dc_file:
        dc_csv_writer = csv.writer(dc_file)
        dc_csv_writer.writerow(['DC_Number','Latitude', 'Longitude'])
        i = 0
        while  i < len(DC_array):
            dc_csv_writer.writerow([DC_array[i][0], DC_array[i][1][0], DC_array[i][1][1]])
            i += 1
           
    with open('./public/data/Facilities.csv', mode='w', newline='') as facilities_file:
        facilities_csv_writer = csv.writer(facilities_file)
        facilities_csv_writer.writerow(['Facility_Number','Latitude', 'Longitude'])
        i = 0
        while  i < len(Facilities_array):
            facilities_csv_writer.writerow([Facilities_array[i][0], Facilities_array[i][1][0], Facilities_array[i][1][1]])
            i += 1
    
    """ring"""
    zlplotnumbered=[]
    ZLPlot_array=[]
    with open('./public/data/ZLPlot.csv', mode='w', newline='') as zlplot_file:
            zlplot_csv_writer = csv.writer(zlplot_file)
            zlplot_csv_writer.writerow(['ZeroLevelPlot','Point1 Latitude', 'Point1 Longitude', 'Point1 Name', 'Point2 Latitude', 'Point2 Longitude', 'Point2 Name', 'Point3 Latitude', 'Point3 Longitude', 'Point3 Name'])
            zlnum = 0
            i = 0
            while i < len(Sorted_ring[1]):
                first = i
                second = i + 1
                if second >= len(Sorted_ring[1]):
                    second = 0
                thiszlplot=[]
                ZLPlot_Number = 'ZL' + str(zlnum).zfill(4)
                point1=[]
                point2=[]
                point3=[]  
                point1.append(Sorted_ring[0][0][1][0])
                point1.append(Sorted_ring[0][0][1][1])
                point2.append(Sorted_ring[1][first][1][0])
                point2.append(Sorted_ring[1][first][1][1])
                point3.append(Sorted_ring[1][second][1][0])
                point3.append(Sorted_ring[1][second][1][1])
                #thiszlplot.append(ZLPlot_Number) 
                thiszlplot.append(point1)
                thiszlplot.append(point2)
                thiszlplot.append(point3)
                zlplotnumbered.append(thiszlplot)
                thiszlplotarray= []
                thiszlplotarray.append(ZLPlot_Number)
                point1_name=get_name(Facilities_array, DC_array, point1)
                thiszlplotarray.append(point1_name)
                thiszlplotarray.append(point1)
                point2_name=get_name(Facilities_array, DC_array, point2)
                thiszlplotarray.append(point2_name)
                thiszlplotarray.append(point2)
                point3_name=get_name(Facilities_array, DC_array, point3)
                thiszlplotarray.append(point3_name)
                thiszlplotarray.append(point3) 
                ZLPlot_array.append(thiszlplotarray) 
                zlnum += 1
                zlplot_csv_writer.writerow([ZLPlot_Number, point1[0], point1[1], point1_name, point2[0], point2[1], point2_name, point3[0], point3[1], point3_name])
                if zlplotlabel == 'show':
                    Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = 'blue', fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, permanent=True, direction='center')).add_to(folium_map)
                else:
                    Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = 'blue', fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, direction='center')).add_to(folium_map) 
                i += 1
            i = 2
            while i < len(hexagon): 
                j = 0
                """side"""
                this='top'                    
                while j < len(hexagon[i]):
                    k = 0
                    """point in side"""
                    while k < len(hexagon[i][j]):
                        thisringindex = i
                        prevringindex = i - 1
                        
                        this = 'top'
                            
                        first = k
                        firstside=j
                        second = k+1
                        secondside=j
                        if second >= len(hexagon[i][j]):
                            second=0
                            secondside=j+1
                            if secondside >=6:
                                secondside = 0
                
                        prevfirst = k
                        prevfirstside = j   
                        if prevfirst >= len(hexagon[i-1][j]):
                            prevfirst = 0
                            prevfirstside = j+1
                            if prevfirstside >= 6:
                                prevfirstside=0
                        
                        prevsecond = k + 1
                        prevsecondside = j
                        if prevsecond >= len(hexagon[i-1][j]):
                            prevsecond = 0
                            prevsecondside = j+1
                            if prevsecondside >= 6:
                                prevsecondside=0
                                
                        thiszlplot=[]
                        ZLPlot_Number = 'ZL' + str(zlnum).zfill(4)
                        point1=[]
                        point2=[]
                        point3=[]  
                        point1.append(hexagon[i][firstside][first][0])
                        point1.append(hexagon[i][firstside][first][1])
                        point1_name=hexagon[i][firstside][first][4]
                        point2.append(hexagon[i][secondside][second][0])
                        point2.append(hexagon[i][secondside][second][1])
                        point2_name=hexagon[i][secondside][second][4]
                        point3.append(hexagon[i-1][prevfirstside][prevfirst][0])
                        point3.append(hexagon[i-1][prevfirstside][prevfirst][1])
                        point3_name=hexagon[i-1][prevfirstside][prevfirst][4]
                        #thiszlplot.append(ZLPlot_Number)
                        thiszlplot.append(point1)
                        thiszlplot.append(point2)
                        thiszlplot.append(point3)
                        zlplotnumbered.append(thiszlplot)
                        thiszlplotarray= []
                        thiszlplotarray.append(ZLPlot_Number)
                        point1_name=get_name(Facilities_array, DC_array, point1)
                        thiszlplotarray.append(point1_name)
                        thiszlplotarray.append(point1)
                        point2_name=get_name(Facilities_array, DC_array, point2)
                        thiszlplotarray.append(point2_name)
                        thiszlplotarray.append(point2)
                        point3_name=get_name(Facilities_array, DC_array, point3)
                        thiszlplotarray.append(point3_name)
                        thiszlplotarray.append(point3) 
                        ZLPlot_array.append(thiszlplotarray) 
                        zlnum += 1
                        zlplot_csv_writer.writerow([ZLPlot_Number, point1[0], point1[1], point1_name, point2[0], point2[1], point2_name, point3[0], point3[1], point3_name])
                        if (point1_name[0:2] == 'FC') & (point2_name[0:2] == 'FC' ) & (point3_name[0:2] == 'FC' ):
                            codedcolor='black'
                            fillcolorcode = 'red'
                        else:
                            codedcolor='black'
                            fillcolorcode = 'blue'
                        if zlplotlabel == 'show':
                            Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = fillcolorcode, fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, permanent=True, direction='center')).add_to(folium_map)
                        else:
                            Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = fillcolorcode, fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, direction='center')).add_to(folium_map) 
                        this='bot'
                            
                        if k < len(hexagon[i][j]) - 1:
                            thiszlplot=[]
                            ZLPlot_Number = 'ZL' + str(zlnum).zfill(4)
                            point1=[]
                            point2=[]
                            point3=[]  
                            point1.append(hexagon[i][secondside][second][0])
                            point1.append(hexagon[i][secondside][second][1])
                            point1_name=hexagon[i][secondside][second][4]
                            point2.append(hexagon[i-1][prevfirstside][prevfirst][0])
                            point2.append(hexagon[i-1][prevfirstside][prevfirst][1])
                            point2_name=hexagon[i-1][prevfirstside][prevfirst][4]
                            point3.append(hexagon[i-1][prevsecondside][prevsecond][0])
                            point3.append(hexagon[i-1][prevsecondside][prevsecond][1])
                            point3_name=hexagon[i-1][prevsecondside][prevsecond][4]
                            #thiszlplot.append(ZLPlot_Number) 
                            thiszlplot.append(point1)
                            thiszlplot.append(point2)
                            thiszlplot.append(point3)
                            zlplotnumbered.append(thiszlplot)
                            thiszlplotarray= []
                            thiszlplotarray.append(ZLPlot_Number)
                            point1_name=get_name(Facilities_array, DC_array, point1)
                            thiszlplotarray.append(point1_name)
                            thiszlplotarray.append(point1)
                            point2_name=get_name(Facilities_array, DC_array, point2)
                            thiszlplotarray.append(point2_name)
                            thiszlplotarray.append(point2)
                            point3_name=get_name(Facilities_array, DC_array, point3)
                            thiszlplotarray.append(point3_name)
                            thiszlplotarray.append(point3) 
                            ZLPlot_array.append(thiszlplotarray) 
                            zlnum += 1
                            zlplot_csv_writer.writerow([ZLPlot_Number, point1[0], point1[1], point1_name, point2[0], point2[1], point2_name, point3[0], point3[1], point3_name])
                            if (point1_name[0:2] == 'FC') & (point2_name[0:2] == 'FC' ) & (point3_name[0:2] == 'FC' ):
                                codedcolor='black'
                                fillcolorcode = 'red'
                            else:
                                codedcolor='black'
                                fillcolorcode = 'blue'
                            if zlplotlabel == 'show':
                                Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = fillcolorcode, fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, permanent=True, direction='center')).add_to(folium_map)
                            else:
                                Polygon([point1, point2, point3], color='black', weight=2.5, fill_color = fillcolorcode, fill_opacity = 0.2, fill=True).add_child(Tooltip(ZLPlot_Number, direction='center')).add_to(folium_map) 
                            this='top'
                        
                        k +=1
                    j += 1
                i +=1
    
    with open('./public/data/ndPlot.csv', mode='w', newline='') as ndplot_file:
        ndplot_csv_writer = csv.writer(ndplot_file)
        ndplot_csv_writer.writerow(['ZeroLevelPlot', 'nd plot'])
        i=0
        ndnumber=0
        ndplots=[]
        while i < len(zlplotnumbered):
            ndplotsforthiszlplot=divide_into_nd_plot(zlplotnumbered[i], n)
            j=0
            while j < len(ndplotsforthiszlplot):
                ndplots.append(ndplotsforthiszlplot[j])
                if zlplotlabel == 'shownd':
                    Polygon(ndplotsforthiszlplot[j], weight=1).add_to(folium_map)
                ZLPlot_Number = 'ZL' + str(i).zfill(4)
                ndPlot_number = 'ND' + str(ndnumber).zfill(8)
                ndplot_csv_writer.writerow([ZLPlot_Number, ndPlot_number])
                j += 1
                ndnumber += 1
            i += 1  
       
    with open('./public/data/ImpactZones.csv', mode='w', newline='') as impactzone_file:
        impactzone_csv_writer = csv.writer(impactzone_file)
        impactzone_csv_writer.writerow(['DC', 'Primary Impact Zone 1', 'Primary Impact Zone 2', 'Primary Impact Zone 3','Primary Impact Zone 4', 'Primary Impact Zone 5', 'Primary Impact Zone 6', 'Secondary Impact Zone 1', 'Secondary Impact Zone 2', 'Secondary Impact Zone 3', 'Secondary Impact Zone 4', 'Secondary Impact Zone 5', 'Secondary Impact Zone 6'])
        i = 0;
        while i < len(DC_array):
            piz=get_primary_impact_zone(ZLPlot_array, DC_array[i][0])
            j=0
            siz=[]
            while j < len(piz):
                siz.append(get_secondary_impact_zone(ZLPlot_array, piz[j]))
                j += 1                
            impactzone_csv_writer.writerow([DC_array[i][0], piz[0], piz[1], piz[2], piz[3], piz[4], piz[5], siz[0], siz[1], siz[2], siz[3], siz[4], siz[5]])
            i += 1

    radius_in_km = 0
    
    i=0
    
    l1plotnumbered=[]
    L1Plot_array=[]
    with open('./public/data/L1Plot.csv', mode='w', newline='') as l1plot_file:
        l1plot_csv_writer = csv.writer(l1plot_file)
        l1plot_csv_writer.writerow(['L1Plot', 'zl plot'])
        i=2
        l1num=0
        l1plots=[]
        while i < len(hexagon): 
            j = 0
            #side
            this='top'                    
            while j < len(hexagon[i]):
                k = 0
                #point in side
                while k < len(hexagon[i][j]):
                    thisringindex = i
                    prevringindex = i - 2
                      
                    this = 'top'
                          
                    first = k
                    firstside=j
                    second = k+2
                    secondside=j
                    if second >= len(hexagon[i][j]):
                        second=0
                        secondside=j+1
                        if secondside >=6:
                            secondside = 0
                
                    prevfirst = k
                    prevfirstside = j   
                    if i == 2:
                        prevfirst = 0
                        prevfirstside = j+1
                        if prevfirstside >= 6:
                            prevfirstside=0
                    elif prevfirst >= len(hexagon[i-2][j]):
                        prevfirst = 0
                        prevfirstside = j+1
                        if prevfirstside >= 6:
                            prevfirstside=0
                        
                    prevsecond = k + 2
                    prevsecondside = j
                    if i == 2:
                        prevsecond = 0
                        prevsecondside = j+1
                        if prevsecondside >= 6:
                            prevsecondside=0
                    elif prevsecond >= len(hexagon[i-2][j]):
                        prevsecond = 0
                        prevsecondside = j+1
                        if prevsecondside >= 6:
                            prevsecondside=0
                                
                        thisl1plot=[]
                        L1Plot_Number = 'L1' + str(l1num).zfill(4)
                        point1=[]
                        point2=[]
                        point3=[]  
                        point1.append(hexagon[i][firstside][first][0])
                        point1.append(hexagon[i][firstside][first][1])
                        point1_name=hexagon[i][firstside][first][4]
                        point2.append(hexagon[i][secondside][second][0])
                        point2.append(hexagon[i][secondside][second][1])
                        point2_name=hexagon[i][secondside][second][4]
                        if i == 2:
                            point3_name = 'DC000'
                            point3.append(Sorted_ring[0][0][1][0])
                            point3.append(Sorted_ring[0][0][1][1])
                        else:
                            point3.append(hexagon[i-2][prevfirstside][prevfirst][0])
                            point3.append(hexagon[i-2][prevfirstside][prevfirst][1])
                            point3_name=hexagon[i-2][prevfirstside][prevfirst][4]
                        #thiszlplot.append(ZLPlot_Number)
                        thisl1plot.append(point1)
                        thisl1plot.append(point2)
                        thisl1plot.append(point3)
                        l1plotnumbered.append(thisl1plot)
                        thisl1plotarray= []
                        thisl1plotarray.append(L1Plot_Number)
                        point1_name=get_name(Facilities_array, DC_array, point1)
                        thisl1plotarray.append(point1_name)
                        thisl1plotarray.append(point1)
                        point2_name=get_name(Facilities_array, DC_array, point2)
                        thisl1plotarray.append(point2_name)
                        thisl1plotarray.append(point2)
                        point3_name=get_name(Facilities_array, DC_array, point3)
                        thisl1plotarray.append(point3_name)
                        thisl1plotarray.append(point3) 
                        L1Plot_array.append(thisl1plotarray) 
                        l1num += 1
                        l1plot_csv_writer.writerow([L1Plot_Number, point1[0], point1[1], point1_name, point2[0], point2[1], point2_name, point3[0], point3[1], point3_name])
                        this='bot'
                            
                        if k < len(hexagon[i][j]) - 1:
                            thisl1plot=[]
                            L1Plot_Number = 'L1' + str(l1num).zfill(4)
                            point1=[]
                            point2=[]
                            point3=[]  
                            point1.append(hexagon[i][secondside][second][0])
                            point1.append(hexagon[i][secondside][second][1])
                            point1_name=hexagon[i][secondside][second][4]
                            if i == 2:
                                point2_name = 'DC000'
                                point2.append(Sorted_ring[0][0][1][0])
                                point2.append(Sorted_ring[0][0][1][1])
                            else:
                                point2_name=hexagon[i-2][prevfirstside][prevfirst][4]
                                point2.append(hexagon[i-2][prevfirstside][prevfirst][0])
                                point2.append(hexagon[i-2][prevfirstside][prevfirst][1])
                            if i == 2:
                                point3_name = 'DC000'
                                point3.append(Sorted_ring[0][0][1][0])
                                point3.append(Sorted_ring[0][0][1][1])
                            else:
                                point3.append(hexagon[i-2][prevsecondside][prevsecond][0])
                                point3.append(hexagon[i-2][prevsecondside][prevsecond][1])
                                point3_name=hexagon[i-2][prevsecondside][prevsecond][4]
                                
                            #thiszlplot.append(ZLPlot_Number) 
                            thisl1plot.append(point1)
                            thisl1plot.append(point2)
                            thisl1plot.append(point3)
                            l1plotnumbered.append(thisl1plot)
                            thisl1plotarray= []
                            thisl1plotarray.append(L1Plot_Number)
                            point1_name=get_name(Facilities_array, DC_array, point1)
                            thisl1plotarray.append(point1_name)
                            thisl1plotarray.append(point1)
                            point2_name=get_name(Facilities_array, DC_array, point2)
                            thisl1plotarray.append(point2_name)
                            thisl1plotarray.append(point2)
                            point3_name=get_name(Facilities_array, DC_array, point3)
                            thisl1plotarray.append(point3_name)
                            thisl1plotarray.append(point3) 
                            L1Plot_array.append(thisl1plotarray) 
                            l1num += 1
                            l1plot_csv_writer.writerow([L1Plot_Number, point1[0], point1[1], point1_name, point2[0], point2[1], point2_name, point3[0], point3[1], point3_name])
                                                    
                    k +=2
                j += 2
            i +=2
    return [folium_map, radius_in_km]


def plotkringcoloured(latitude, longitude, granularity, hexagons): 
    start_coords = (latitude, longitude)
    folium_map = folium.Map(location=start_coords, zoom_start=granularity, zoom_control=True)
    tooltip = 'Click me!'
    #Marker([latitude, longitude], popup='<i>Coimbatore</i>', tooltip=tooltip).add_to(folium_map)
    latitudes=[]
    longitudes=[]
    nodetype=[]
    hexagons.sort(key=lambda x: (x[0],x[1]))
    i=0
    while i < len(hexagons):
        latitudes.append(hexagons[i][0])
        longitudes.append(hexagons[i][1])
        tooltip=i
        Marker([latitudes[i], longitudes[i]], popup='<i>hexagon point</i>', tooltip=tooltip).add_to(folium_map)
        i += 1
    #Polygon(zip(longitudes, latitudes)).add_to(folium_map)
    #Polygon(hexagons).add_to(folium_map)
    return folium_map

def distance_in_km(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
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
    return(c * r) 

def get_midpoint(lat1,lon1,lat2,lon2):

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
    
    
    return [lat3, lon3]

def divide_into_4(triangle):
    p1 = triangle[0]
    p2 = triangle[1]
    p3 = triangle[2]
    p4 = get_midpoint(triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1])
    p5 = get_midpoint(triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1])
    p6 = get_midpoint(triangle[2][0], triangle[2][1], triangle[0][0], triangle[0][1])
    return [[p1,p4,p6],[p4,p5,p6],[p2,p4,p5],[p3,p5,p6]]

def divide_into_nd_plot(triangle, n):
    thisleveltriangles=[]
    thisleveltriangles.append(triangle)
    j=0
    while j < n:
        i = 0
        k=len(thisleveltriangles)
        trianglestodivide=thisleveltriangles
        thisleveltriangles=[]
        while i < k:
            dividedtriangles = divide_into_4(trianglestodivide[i])
            thisleveltriangles.append(dividedtriangles[0])
            thisleveltriangles.append(dividedtriangles[1])
            thisleveltriangles.append(dividedtriangles[2])
            thisleveltriangles.append(dividedtriangles[3])
            i = i+1
        j += 1
        
    return thisleveltriangles

def get_name(array1, array2, searchitem):
    i = 0
    while i < len(array1):
        if array1[i][1] == searchitem:
            return array1[i][0]
        i += 1
    i = 0
    while i < len(array2):
        if array2[i][1] == searchitem:
            return array2[i][0]
        i += 1


def get_primary_impact_zone(array, dc):
    i = 0
    iz=[]
    while i < len(array):
        if (array[i][1] == dc) | (array[i][3] == dc) | (array[i][5] == dc):
            iz.append(array[i][0])
        i += 1
    return iz  

def get_secondary_impact_zone(array, piz):
    i=0
    iz=[]
    fac=[]
    while i < len(array):
        if array[i][0] == piz:
            if array[i][1][0:2] == 'FC':
                fac.append(array[i][1])
            if array[i][3][0:2] == 'FC':
                fac.append(array[i][3]) 
            if array[i][5][0:2] == 'FC':
                fac.append(array[i][5])
        i += 1
    i = 0
    while i < len(array):
        if ((((fac[0] == array[i][1]) | (fac[0] == array[i][3]) | (fac[0] == array[i][5])) & ((fac[1] == array[i][1]) | (fac[1] == array[i][3]) | (fac[1] == array[i][5]))) & (array[i][0] != piz)):
            return array[i][0]
        i += 1
    
    
        

