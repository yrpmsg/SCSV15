from server import app
from math import floor, pow
from flask import Flask, request, render_template, redirect, url_for, flash
import time
from math import pow
import os
#import magic
import urllib.request
from werkzeug.utils import secure_filename
from ..functions.scsutils import CalculatePopulationMigration


ALLOWED_EXTENSIONS = set(['csv'])
UPLOAD_FOLDER = './public/data'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/PopMigration')
def popmigration_form():
    return render_template('popmigration.html')

@app.route('/PopMigration', methods=['POST'])
def PopMigration():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'populationdata' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['populationdata']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'population.csv'))
            flash('File successfully uploaded')
            return redirect('/PopMigrationProcess')
        else:
            flash('Allowed file type is csv')
            return redirect(request.url)

@app.route('/PopMigrationProcess', methods=["GET"])
def popmigrationprocess_form():
    print('popmigrationprocess_form')
    return render_template('popmigrationin.html')

@app.route('/PopMigrationProcess', methods=['GET', 'POST'])
def PopMigrationProcess():
    print('popmigrationprocess')
    if request.method == 'POST':
        print('popmigrationprocess-inside-if')
        # check if the post request has the file part
        Rmax = int(request.form["Rmax"])
        CalculatePopulationMigration(Rmax)
        return render_template('popmigrationout.html')
    else:    
        return render_template('popmigrationin.html')