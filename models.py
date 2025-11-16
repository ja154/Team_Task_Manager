from extensions import db
from flask_login import UserMixin ## to make the user model compatible with flask_login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) ## primary key
    username = db.Column(db.String(150 ), unique=True, nullable=False) ## username
    email = db.Column(db.String(150), unique=True, nullable=False) ## email
    password = db.Column(db.String(150), nullable=False) ## password
    role = db.Column(db.String(15), default = 'member') ## role
    created_task = db.relationship('Task', backref='creator', foreign_key='Task.created_by', lazy=True) ## created tasks linking users with tasks they  create
    shared_tasks = db.relationship('Task', backref='receiver', foreign_key='Task.shared_with', lazy=True) ## shared tasks linking users with tasks they are shared with

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True) ## primary key
    title = db.Column(db.String(200), nullable=False) ## title
    description = db.Column(db.Text, nullable=False) ## description in text to allow for long form content in this field
    status = db.Column(db.String(20), default = 'pending') ## status of the task by default all tasks start with the status pending
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) ## created by linking tasks to users
    shared_with = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) ## shared with linking tasks to users
##so in summary the primary key is linked with the foreign key through the task model and the foreign key is linked with the primary key through the user model