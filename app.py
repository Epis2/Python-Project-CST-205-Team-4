# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
# create the application object
app = Flask(__name__)

users = {
    'admin': {
        'password' : 'admin',
    }

}
# use decorators to link the function to a url
@app.route('/')
def welcome():
    return render_template('welcome.html')  # render a template


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if(request.form['username'] in users and request.form['password'] == users[request.form['username']]['password']):
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        users[request.form['username']] = {
            'password': request.form['password'],
        }
        return redirect(url_for('welcome'))
    return render_template('create.html')
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
