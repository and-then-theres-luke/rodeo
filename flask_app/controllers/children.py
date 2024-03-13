from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import chore, parent, child

@app.route('/children')
def children_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    all_children = child.Child.get_all_children_by_parent_id(session['user_id'])
    return render_template('manage_children.html', all_my_children = all_children)

@app.route('/children/view/<int:id>')
def view_one_child_frontend(id):
    if 'user_id' not in session:
        return redirect('/login')
    one_child = child.Child.get_child_by_id(id)
    return render_template("edit_child.html", one_child = one_child)
    
    
@app.post('/children/add/process')
def add_child_frontend():
    if 'user_id' not in session:
        return redirect('/login')
    child.Child.create_child(request.form)
    return redirect('/children')
    
@app.route('/children/delete/process/<int:id>')
def remove_child_frontend(id):
    if 'user_id' not in session:
        return redirect('/login')
    child.Child.delete_child(id)
    return redirect('/children')