from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import chore, parent # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Chores Controller


@app.route('/chores/create')
def create_chore_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    return redirect('/chore/page')

@app.post('/chores/create/process')
def create_chore_process_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    if not chore.Chore.create_chore(request.form):
        return redirect('/chore/create')
    return redirect('/dashboard')


# Read Chores Controller

@app.route('/chores')
def view_all_chores_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    all_chores = chore.Chore.get_all_chores_by_parent_id(session['user_id'])
    return render_template('view_all_chores.html', all_chores = all_chores)
    

@app.route('/chores/view/<int:chore_id>')
def view_one_chore_frontend(chore_id):
    if 'user_id' not in session: 
        return redirect('/')
    one_chore = chore.Chore.get_chore_by_id(chore_id)
    if one_chore.parent_id != session['user_id']:
        return redirect('/dashboard')
    return render_template('chores_home.html')

# Update Chores Controller

@app.post("/chores/update/process")
def chore_update_process_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    chore.Chore.delete_chore(request.form['chore_id'])
# Delete Chores Controller



# Update Chores Controller



# Delete Chores Controller



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