# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
from base64 import b64decode
from random import randint
#import datetime as dt
#import json
import os
# pip install
from flask import Flask, render_template, request, redirect, url_for
from yaml import dump
# same project
from ghub import upload_images_to_github, upload_stats_to_github

PATH_FOR_IMAGES =  './static/bodyparts' #r'C:\n4\znv\CO1111\k2'
PATH_FOR_DATA = './s'

def savef( path, text ):
    with open( path, 'w', encoding='utf-8' ) as f:
        f.write(text)
    log.info( 'saved file %s'%path )
    
def savef_yaml( path, data ):
    with open( path, 'w', encoding='utf-8' ) as f:
        dump( data, f )
    log.info( 'saved file %s'%path )
    
def get_bodypart( bodypart, f=None ):
    
    root = None
    subfolder = None
    if bodypart=='head':
        #root = os.path.join( PATH_FOR_IMAGES,'0' )
        subfolder = '0'
    elif bodypart=='body':
        #root = os.path.join( PATH_FOR_IMAGES,'1' )
        subfolder = '1'
    if bodypart=='tail':
        #root = os.path.join( PATH_FOR_IMAGES,'2' )
        subfolder = '2'
    root = '/'.join( [PATH_FOR_IMAGES,subfolder] )
    
    # i know exact filename
    if not f is None:
        src = os.path.join( root,f )
        if os.path.isfile(src):
            # it actually exists
            return url_for( 'static',filename='bodyparts/%s/%s'%(subfolder,f) )
    
    # ill choose random
    fs = os.listdir( root )
    
    # ive got nothing to choose from
    if len(fs)==0: return ''
    
    # i have something to choose from
    iloc = randint( 0, len(fs)-1 )
    return url_for( 'static',filename='bodyparts/%s/%s'%(subfolder,fs[iloc]) )

def determine_animal_structure( bodyparts ):
    
    # Checks missing bodyparts and
    # defines proper layout.
    
    # At least one bodypart is present.
    
    nohead = bodyparts[0]==''
    nobody = bodyparts[1]==''
    notail = bodyparts[2]==''
    
    text = ''
    ilocs = ()
    
    if nohead&nobody:
        text = '?!'
        ilocs = (2,2) # two mirrored tails
    elif nohead&notail:
        text = 'a centipede?'
        ilocs = (1,1,1,1,1) # lots of bodies
    elif nobody&notail:
        text = 'hmm'
        ilocs = (0,0) # two mirrored heads
    else:
        text = 'ultimate jackrabbit'
        ilocs = (0,1,2) # three parts
    return text, ilocs

def save_base64_image( path, data ):
    
    # help:
    # https://stackoverflow.com/questions/34116682/save-base64-image-python
    # https://stackoverflow.com/questions/45879045/binascii-error-incorrect-padding-even-when-string-length-is-multiple-of-4
    
    im = b64decode( data.partition(',')[2] )
    with open( path, 'wb' ) as f:
        f.write(im)

# help:
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

app = Flask(__name__)

@app.route( '/' )
def home():
    return "AAAAAAAAAAAAA"

@app.route("/draw")
def draw():
    return render_template("draw.html")

@app.route("/result")
@app.route("/result/<f>")
def result( f=None ):
    
    # choose some bodyparts
    bodyparts = [
        get_bodypart( 'head',f=f ),
        get_bodypart( 'body',f=f ),
        get_bodypart( 'tail',f=f )
        ]
    
    # adapt for missing parts
    text, ilocs = determine_animal_structure( bodyparts )
    
    # prepare template inserts
    img_srcs = [ bodyparts[iloc] for iloc in ilocs ]
    
    return render_template(
        "result.html",
        image_srcs=img_srcs,
        stamp=text,
        )

@app.route( '/upload', methods=['GET','POST'] )
def upload():
    
    # help:
    # https://stackoverflow.com/questions/51035478/how-to-upload-a-file-using-javascript
    
    if request.method == 'POST':
        
        # i finished drawing jackrabbit
        # and pressed the submit button
    
        # unique user id and bodypart iloc
        bodypartiloc = request.form['bodypartiloc']
        
        # save image
        f = '%s___%s.png'%(
            request.form['user_id'],
            request.form['timestamp']
            )
        src0 = os.path.join(
            PATH_FOR_IMAGES,
            str(bodypartiloc),
            f
            )
        save_base64_image( src0, request.form['image64'] )
        #print(src0)
        
        # save stats
        
        src1 = os.path.join(
            PATH_FOR_DATA,
            '%s___%s%s.yaml'%(
                request.form['user_id'],
                request.form['timestamp'],
                'kb'
                )
            )
        savef( src1, request.form['stats_keyboard'] )
        #print(src1)
        
        src2 = os.path.join(
            PATH_FOR_DATA,
            '%s___%s%s.yaml'%(
                request.form['user_id'],
                request.form['timestamp'],
                'ui'
                )
            )
        savef( src2, request.form['stats_ui'] )
        #print(src2)
        
        # save metadata
        src = os.path.join(
            PATH_FOR_DATA,
            '%s___%s.yaml'%(
                request.form['user_id'],
                request.form['timestamp'],
                )
            )
        data = {
            'user id': request.form['user_id'],
            'bodypart': bodypartiloc,
            'user agent': request.form['user_agent'],
            'kb stats': src1,
            'ui stats': src2,
            'im': src0,
            }
        savef_yaml( src, data )
        #print(src)
        
        # upload just saved files to private github storage
        # these files will not be accessibl ein the app
        # and will not be automatically deleted by heroku
        #upload_stats_to_github( [src1,src2,src] )
        #upload_images_to_github( [src0] )
        
        # show result with current bodypart
        # help:
        # https://www.askpython.com/python-modules/flask/flask-redirect-url
        return redirect( f'/result/{f}' )

    #return render_template('upload.html')
    
#---------------+++
# Autorun.

if __name__ == '__main__':
    app.run( debug=True )

#---------------------------------------------------------------------------+++
# end 2022.04.10
# added github file uploading