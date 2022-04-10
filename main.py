# -*- coding: utf-8 -*-

#---------------------------------------------------------------------------+++
#

# logging
import logging
log = logging.getLogger(__name__)

# embedded in python
from random import randint
# pip install
from flask import Flask, render_template, request, redirect
# same project
from ghub import ( write_file_to_github, load_file_from_github,
    list_files_in_github )

#-------------------+++
# Definitions.

def get_bodypart( bodypart, f=None ):
    
    subfolder = None
    if bodypart=='head': subfolder = '0'
    elif bodypart=='body': subfolder = '1'
    elif bodypart=='tail': subfolder = '2'
    
    srcs = list_files_in_github( subfolder )
    
    # i know exact filename
    if not f is None:
        
        for src in srcs:
            if f in src:
                # it actually exists
                data = load_file_from_github( src )
                return data
    
    # ill choose random
    
    # ive got nothing to choose from
    if len(srcs)==0: return ''
    
    # i have something to choose from
    iloc = randint( 0, len(srcs)-1 )
    data = load_file_from_github( srcs[iloc] )
    return data

def determine_animal_structure( bodyparts ):
    
    # Checks missing bodyparts and
    # defines proper layout.
    
    # At least one bodypart is present.
    
    nohead = bodyparts[0]==''
    nobody = bodyparts[1]==''
    notail = bodyparts[2]==''
    
    text = ''
    ilocs = ()
    
    if nohead&nobody&notail:
        text = 'a ghost'
        ilocs = () # nothing
    elif nohead&nobody:
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

#-------------------+++
# Actual code.

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
    
    for bp in bodyparts:
        print( len(bp) )
    
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
        src0 = '%s/%s'%(
            bodypartiloc,
            f
            )
        write_file_to_github( src0, request.form['image64'] )
        
        # save stats
        
        src1 = 's/%s___%s%s.yaml'%(
            request.form['user_id'],
            request.form['timestamp'],
            'kb'
            )
        write_file_to_github( src1, request.form['stats_keyboard'] )
        
        src2 = 's/%s___%s%s.yaml'%(
            request.form['user_id'],
            request.form['timestamp'],
            'ui'
            )
        write_file_to_github( src2, request.form['stats_ui'] )
        
        # save metadata
        src = 's/%s___%s.yaml'%(
            request.form['user_id'],
            request.form['timestamp'],
            )
        data = {
            'user id': request.form['user_id'],
            'bodypart': bodypartiloc,
            'user agent': request.form['user_agent'],
            'kb stats': src1,
            'ui stats': src2,
            'im': src0,
            }
        write_file_to_github( src, str(data) )
        
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