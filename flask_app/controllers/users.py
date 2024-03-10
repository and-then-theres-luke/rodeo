from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller


@app.post('/user/register')
def create_new_user():
    if user.User.create_new_user(request.form):
        return redirect('/#') # redirect to the show page
    return redirect('/')




# Read Users Controller

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/#')
def display_user_page():
    print(session, "This is session") 
    if 'user_id' not in session: return redirect('/')
    user_data = user.User.get_user_by_id(session['user_id'])
    # you will need a function to get info from the joining table here
    return render_template('#.html', user = user_data, )
    


# Update Users Controller

@app.post('/user/update')
def update_user_account():
    if 'user_id' not in session: return redirect('/')
    user.User.update_user_info(request.form)
    return redirect('/user/account')

# Delete Users Controller

@app.post('/user/account/delete')
def delete_user_account():
    if 'user_id' not in session: return redirect('/')
    user.User.delete_user_account(session['user_id'])
    session.clear()
    return redirect('/')

# login user

@app.post('/user/login')
def log_user_in():
    if user.User.log_user_in(request.form):
        return redirect('/#') # redirect to the show page
    return redirect('/')


# log user out

@app.route('/user/logout')
def log_user_out():
    session.clear()
    return redirect('/')


# Update Users Controller



# Delete Users Controller



# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.