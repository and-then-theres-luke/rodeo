from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import chore, parent, child # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Chores Controller


@app.route('/chores/create')
def create_chore_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    all_children = child.Child.get_all_children()
    if session['is_parent'] == False:
        return redirect('/')
    return render_template('create_chore.html', children=all_children)

@app.post('/chores/create/process')
def create_chore_process_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    if not chore.Chore.create_chore(request.form):
        return redirect('/chores/create')
    return redirect('/dashboard')



# Read Chores Controller

@app.route('/chores')
def view_all_chores_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    all_chores = chore.Chore.get_all_chores_by_parent_id(session['user_id'])
    if session['is_parent'] == True:
        one_user = parent.Parent.get_parent_by_id(session['user_id'])
        return render_template('all_chores.html', all_chores = all_chores, one_user = one_user)
    else:
        one_user = child.Child.get_child_by_id(session['user_id'])
        return render_template('all_chores.html', all_chores = all_chores, one_user = one_user)
    

@app.route('/chores/view/<int:chore_id>')
def view_one_chore_frontend(chore_id):
    if 'user_id' not in session: 
        return redirect('/')
    one_chore = chore.Chore.get_chore_by_id(chore_id)
    all_children = child.Child.get_all_children_by_parent_id(session['user_id'])
    print(one_chore,"ONECHORE")
    if one_chore.parent_id != session['user_id']:
        return redirect('/dashboard')
    return render_template('view_one_chore.html', one_chore = one_chore, all_children = all_children)



# Update Chores Controller

@app.route('/chore/complete/<int:chore_id>')
def toggle_completed_frontend(chore_id):
    if 'user_id' not in session: 
        return redirect('/')
    chore.Chore.toggle_complete(chore_id)
    return redirect('/dashboard')

@app.post("/chores/update/process")
def chore_update_process_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    print(request.form,"!!!!!!!!@##@#$$@@@@@@@@@@@@@@")
    chore.Chore.edit_chore(request.form)
    return redirect('/dashboard')

# Delete Chores Controller

@app.get("/chores/delete/<int:chore_id>")
def chore_delete_frontend(chore_id):
    if 'user_id' not in session: 
        return redirect('/')
    chore.Chore.delete_chore(chore_id)
    return redirect('/dashboard')




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