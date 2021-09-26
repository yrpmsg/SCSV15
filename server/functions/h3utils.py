from h3 import h3

def gethexagon(latitude, longitude, granularity):
    h3_address = h3.geo_to_h3(latitude, longitude, granularity) # lat, lng, hex resolution
    hex_center_coordinates = h3.h3_to_geo(h3_address) # array of [lat, lng]
    hex_boundary = h3.h3_to_geo_boundary(h3_address) # array of arrays of [lat, lng]
    print(hex_boundary)
    return hex_boundary # resolution 8

def getkrings(latitude, longitude, granularity, radius):
    h3_address = h3.geo_to_h3(latitude, longitude, granularity) # lat, lng, hex resolution
    kring = h3.k_ring(h3_address, radius) # a collection of hexagons within kring sizes from 0 to 3
    print("k ring")
    print(kring)
    out = []
    for geoloc in kring:
        kringgeo=h3.h3_to_geo(geoloc)
        out.append(kringgeo)

    print("out")
    print(out) 
    return out # resolution 8

def getkringdistances(latitude, longitude, granularity, radius):
    h3_address = h3.geo_to_h3(latitude, longitude, granularity) # lat, lng, hex resolution
    kring_distances = h3.k_ring_distances(h3_address, radius) # a collection of hexagons within kring sizes from 0 to 3
    print("k ring distances")
    print(kring_distances)
#    out1 = [set() for _ in range(4)]
#    i=0
#    while i < 4:
#        for geoloc in kring_distances[i]:
#            kringgeo=h3.h3_to_geo(geoloc)
#            out1[i].update(kringgeo)
#        i+=1

#    print("out1")
#    print(out1)
#    return out1 # resolution 8
    out = []
    i=0
    while i < radius:
        for geoloc in kring_distances[i]:
            kringgeo=h3.h3_to_geo(geoloc)
            out.append(kringgeo)
        i+=1
    print("out")
    print(out) 
    return out # resolution 8


def getpolyfill(latitude, longitude, granularity, radius):
    #this code does not work
    h3_address=h3.geo_to_h3(latitude, longitude, granularity)
    main_hexagon=h3.h3_to_geo_boundary(h3_address)
    print(main_hexagon)
    geoJson = {'type': 'Polygon', 'coordinates': [main_hexagon] }
    hexagons = h3.polyfill(geoJson, radius, geo_json_conformant=False)
    print(hexagons)
    return hexagons