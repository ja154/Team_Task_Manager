from math import log
import re
from app.models import User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from exttensions import db
from modelsTask,  imoport User, Task

app = Flask(__name__) ##initialising the flask app
app.config['SECRET_KEY'] = 'testkey' ##secret key for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db' ##database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ##to supress the warning and saves on memory


db.init_app(app) ##initialising the database or pluging in the db to the main app system
##initialising the flask login manager system
login_manager = LoginManager() ##initialising the login manager
login_manager.login_view = 'login' ##login view
login_manager.init_app(app) ##initialising the login manager

##flask login user loader function to load the user from the database using user id 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) ##load the user from the database


## routes for the app

@app.route('/') ##default route
def home():
    return redirect(url_for('login')) ##redirect to login page automatically

##register route 
@app.route('/register', methods=['GET', 'POST']) ##register route.
def register():
    if request.method == 'POST': ##if the request method is post
        username = request.form.get('username') ##get the username from the form
        password = generate_password_hash(request.form['password']) ##hash the password 
        role = request.form.get('role','member') ##get the role from the form
        email = request.form.get('email') ##get the email from the form
        
        if User.query.filter_by(username=username).first(): ##check if the username already exists
            flash('Username already exists','error') ##flash error message
            return redirect(url_for('register')) ##redirect to register page
        
        ##if new user data is saved in the db
        
        new_user = User(username=username, password=password, role=role, email=email) ##create new user object
        db.session.add(new_user) ##add new user to the session
        db.session.commit() ##commit the session
        flash('Registration successful! Please log in.','success')
        return redirect(url_for('login')) ##redirect to login page
    return render_template('register.html') ##render the register template

##login route

@app.route('/login', methods=['GET', 'POST']) ##login route
def login():
    if request.method == 'POST': ##if the request method is post
        username = request.form.get('username') ##get the username from the form
        password = request.form.get('password') ##get the password from the form
        user = User.query.filter_by(username=username).first() ##query the user from the database
        
    if user and check_password_hash(user.password, password): ##if user exists and password is correct
        login_user(user) ##login the user
        return redirect(url_for('admin_dashboard' if user.role == 'admin' else 'dashboard'
    flash('Invalid username or password','error') ##flash error message
    return render_template('login.html'))) ##render the login template

##dashboard route for authorized users

@app.route('/dashboard') ##dashboard route
@login_required ##login required decorator to protect the route
def dashboard():
    my_tasks = Task.query.filter((Task.created_by == current_user.id) | (Task.shared_with == current_user.id)).all() ##query the tasks created by or shared with the current user
    shared_tasks = Task.query.filter_by(shared_with=current_user.id).all() ##query the tasks shared with the current user
    return render_template('dashboard.html', my_tasks=my_tasks, shared_tasks=shared_tasks) ##render the dashboard template with the tasks

##admin dashboard route for admin users

@app.route('/admin') ##admin dashboard route
@login_required ##login required decorator to protect the route
def admin_dashboard():
    if current_user.role != 'admin': ##if the current user is not admin
        flash('Access denied: Admins only.','error') ##flash error message
        return redirect(url_for('dashboard'))
    
    task = Task.query.all() ##query all tasks
    return render_template('admin_dashboard.html', tasks=tasks) ##render the admin dashboard template with the tasks
                     
##add task route

@app.route('/add_task', methods=['GET', 'POST']) ##add task route
@login_required ##login required decorator to protect the route
def add_task():
    if request.method == 'POST':
        title = request.form.get['title'] ##get the title from the form
        description = request.form.get['description'] ##get the description from the form
        shared_with_id = int(request.form['shared_with']) ##get the shared with user id from the form
        new_task = Task(title=title, description=description, created_by=current_user.id, shared_with=shared_with_id)
        
        db.session.add(new_task) ##add new task to the session
        db.session.commit()
        
        flash ('Task added successfully!','success')
        
    users = User.query.filter(User.id != current_user.id).all() ##query all users except the current user
    return render_template('add_task.html', users=users) ##render the add task template with the users
  
  ##edit task route
  
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id) ##get the task by id or return 404
    if task.created_by != current_user.id and current_user.role != 'admin': ##if the current user is not the creator of the task or admin
        flash('Access denied: You can only edit your own tasks.','error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        task.title = request.form['title'] ##update the title
        task.description = request.form['description']
        task.status = request.form['status']
        
        db.session.commit()
        flash('Task updated successfully!','success')
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)

##delete task route

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.created_by != current_user.id and current_user.role != 'admin':
        flash('Access denied: You can only delete your own tasks.','error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully!','success')
    return redirect(url_for('dashboard'))

##logout route

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    