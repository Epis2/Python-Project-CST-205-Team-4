# import the Flask class from the flask module
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import sqlite3
# create the application object
app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')


users = {
    'admin': {
        'password' : 'admin',
    }

}
#logged_in = false
# use decorators to link the function to a url
@app.route('/')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/upload',methods=['GET','POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
    else:
        file_url = None
    return render_template('upload.html', form = form, file_url = file_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if(request.form['username'] in users and request.form['password'] == users[request.form['username']]['password']):

            return redirect(url_for('upload_file'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        users[request.form['username']] = {
            'password': request.form['password'],
        }
        return redirect(url_for('upload_file'))
    return render_template('create.html')
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
