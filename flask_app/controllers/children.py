from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import chore, parent, child

@app.route('/children')
def children_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    all_children = child.Child.get_all_children_by_parent_id(session['user_id'])
    return render_template('manage_children.html', all_children = all_children)
    
@app.post('/children/add/process')
def add_child_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    child.Child.create_child(request.form)
    return redirect('/children')
    
@app.post('/children/delete/process')
def remove_child_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    child.Child.delete_child(request.form['child_id'])
    return redirect('/children')