from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import parent, child, chore # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Users Controller

@app.post('/parent/register')
def create_new_parent_frontend():
    if parent.Parent.create_new_parent(request.form):
        session['is_parent'] = True
        return redirect('/dashboard')
    return redirect('/login')

# Read Users Controller

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    return redirect("/dashboard")

@app.get('/dashboard')
def display_dashboard_frontend():
    if 'user_id' not in session: 
        return redirect('/')
    if session['is_parent'] == True:
        one_user = parent.Parent.get_parent_by_id(session['user_id'])
    else:
        one_user = child.Child.get_child_by_id(session['user_id'])
    all_chores = chore.Chore.get_chore_by_parent_id()
    return render_template('dashboard.html', one_user = one_user, all_chores = all_chores )
    
### login user routes

@app.route('/login')
def login_frontend():
    return render_template('login.html')

@app.post('/login/process')
def login_process_frontend():
    if not parent.Parent.log_parent_in(request.form['email']):
        if not child.Child.log_child_in(request.form['email']):
            return redirect('/login')
    return redirect('/dashboard')

# log user out

@app.route('/logout')
def logout_frontend():
    session.clear()
    return redirect('/login')

# Update Parent Controller

@app.post('/parent/update')
def update_parent_frontend():
    if 'user_id' not in session: 
        return redirect('/login')
    return redirect('/parent/account')

@app.post('/parent/update/process')
def update_parent_process_frontend():
    if 'user_id' not in session: 
        return redirect('/login')
    if session['user_id'] != request.form['user_id']:
        return redirect('/login')
    parent.Parent.update_parent_info(request.form)
    return redirect('/parent/account')


# Delete Users Controller
@app.post('/parent/account/delete')
def delete_user_account_frontend():
    if 'user_id' not in session: return redirect('/')
    parent.Parent.delete_parent_account(session['user_id'])
    session.clear()
    return redirect('/')
