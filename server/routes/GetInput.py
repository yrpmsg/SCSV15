from server import app
from math import floor, pow
from flask import Flask, request, render_template, redirect, url_for
import folium
import h3
import time
from math import pow
#from ..functions.foliumutils import drawonmap
from ..functions.h3utils import getkrings
from ..functions.h3utils import getkringdistances
from ..functions.h3utils import getpolyfill
from ..functions.foliumutils import mapit
from ..functions.foliumutils import plotkring
from ..functions.foliumutils import plotNumberedGridKMNew

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

@app.route('/GetInput', methods=["GET", "POST"])
def GetInput():
    errors = ""
    if request.method == "POST":
        latitude = float(request.form["latitude"])
        longitude = float(request.form["longitude"])
        radius = int(request.form["radius"])
        n = int(request.form["n"])
        zlplotlabel = request.form["zlplotlabel"]
        zoomlevel = int(request.form["zoomlevel"])
        #hexagons = getkringdistances(latitude, longitude, granularity, radius)
        n_to_granularity=[9,8,8,8,7,6,6,6,5,4,3,3,3,2,1,1,1,0]
        granularity = n_to_granularity[n];
        kring = getkrings(latitude, longitude, granularity, radius)
        #hexagons = getpolyfill(latitude, longitude, granularity, radius)
        print(kring)
        values = plotNumberedGridKMNew(latitude, longitude, radius, n, zoomlevel, zlplotlabel, kring)
        folium_map = values[0]
        radius_in_km = values[1]
        print(radius_in_km)
        requestedifd = 0.152 * pow(2, n)
        folium_map.save('./public/map.html')
        time.sleep(5)
        return render_template('foliumflaskinmap.html', radiusinkm=radius_in_km, requestedifd=requestedifd, resolution=granularity)
        #return folium_map._repr_html_()
    else: 
        return render_template('foliumflaskin.html')

@app.route('/Map')
def Map():
    return render_template('map.html')

