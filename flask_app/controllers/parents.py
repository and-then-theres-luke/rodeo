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
    print("session['is_parent']", session['is_parent'])
    if session['is_parent'] == True:
        one_user = parent.Parent.get_parent_by_id(session['user_id'])
        all_chores = chore.Chore.get_all_chores_by_parent_id(session['user_id'])
    else:
        one_user = child.Child.get_child_by_id(session['user_id'])
        all_chores = chore.Chore.get_all_chores_by_parent_id(one_user.parent_id)
    return render_template('dashboard.html', one_user = one_user, all_chores = all_chores )
    
### login user routes

@app.route('/login')
def login_frontend():
    return render_template('login.html')

@app.post('/login/process')
def login_process_frontend():
    if not parent.Parent.log_parent_in(request.form):
        if not child.Child.log_child_in(request.form):
            return redirect('/login')
    return redirect('/dashboard')

# log user out

@app.route('/logout')
def logout_frontend():
    session.clear()
    return redirect('/login')

# Update Parent Controller

@app.route('/parent/account')
def update_parent_frontend():
    if 'user_id' not in session: 
        return redirect('/login')
    one_user = parent.Parent.get_parent_by_id(session['user_id'])
    return render_template('one_user.html', one_user = one_user)

@app.post('/parent/account/process')
def update_parent_process_frontend():
    if 'user_id' not in session: 
        return redirect('/login')
    parent.Parent.edit_parent(request.form)
    return redirect('/parent/account')


# Delete Users Controller
@app.post('/parent/account/delete')
def delete_user_account_frontend():
    if 'user_id' not in session: return redirect('/')
    parent.Parent.delete_parent_account(session['user_id'])
    session.clear()
    return redirect('/')
