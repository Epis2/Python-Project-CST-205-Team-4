# import the Flask class from the flask module
import os
from flask import Flask, render_template, redirect,flash, url_for, request, session, abort
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

import Filters as filter
from PIL import Image


# create the application object
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'I have a dream'
route = os.getcwd() + '/static'
app.config['UPLOADED_PHOTOS_DEST'] = route

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')


users = {
    'admin': {
        'password' : 'admin',
        "photos": []
    }

}
currentUser = "admin"
image = ""
# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('welcome.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global currentUser
    if request.method == 'POST':
        if(request.form['username'] in users and request.form['password'] == users[request.form['username']]['password']):
            currentUser = request.form['username']

            return redirect(url_for('upload_file'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/create', methods=['GET', 'POST'])
def create():
    global currentUser
    if request.method == 'POST':
        currentUser = request.form['username']
        users[currentUser] = {
        "password": request.form['password'],
        "photos": []
        }
        return redirect(url_for('upload_file'))
    return render_template('create.html')

@app.route('/modify',methods=['GET','POST'])
def modify():
    global image
    if request.method == "POST":
        route = 'static/' + image
        if request.form['submit'] == 'Decrease Red':
            filter.decrease_red(route,50)
        elif request.form['submit'] == 'Negative':
            filter.negative(route)
        elif request.form['submit'] == 'greyscale':
            filter.greyscale(route)
        elif request.form['submit'] == 'sepia':
            filter.sepia(route)
        elif request.form['submit'] == 'thumbnail':
            filter.thumbnail(route)
        elif request.form['submit'] == 'crop':
            return redirect(url_for('crop'))
        elif request.form['submit'] == 'Median':
            filter.medianFilter(route)
        elif request.form['submit'] == 'Gotham':
            filter.gotham(route)
        elif request.form['submit'] == 'Write':
            return redirect(url_for('write'))
    return render_template("modify.html",image = image)
@app.route('/crop',methods=['GET','POST'])
def crop():
    global image
    if request.method == "POST":
        route = 'static/' + image
        if request.form['submit'] == 'Crop':
            filter.crop(route,request.form["lLeft"],request.form["uLeft"],request.form["uRight"],request.form["lRight"])
    return render_template("crop.html",image = image)
@app.route('/write',methods=['GET','POST'])
def write():
    global image
    if request.method == "POST":
        route = 'static/' + image
        if request.form['submit'] == 'Write':
            filter.writeText(route,request.form["text"],request.form["x"],request.form["y"],1)
    return render_template("write.html",image = image)
@app.route('/upload',methods=['GET','POST'])
def upload_file():
    form = UploadForm()
    global currentUser
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        temp = file_url.split("/")
        users[currentUser]['photos'].append(temp[-1])
    else:
        file_url = None
    return render_template('upload.html', form = form, file_url = file_url)
@app.route('/pictures', methods=['GET', 'POST'])
def showPictures():
    global currentUser
    global image
    if request.method == 'POST':
        image = request.form['username']
        return redirect(url_for('modify'))
    return render_template('pictures.html',pictureDictionary = users[currentUser]["photos"],currentUser = currentUser)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
