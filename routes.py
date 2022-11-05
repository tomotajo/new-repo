import hashlib
import os
from flask import render_template, send_from_directory, url_for
from flask import render_template, request, redirect, session, flash
from app import app, db
from config import Config
from models import User
from shop_functions import check_login
from datetime import timedelta

from werkzeug.utils import secure_filename


@app.route('/')
def home():
    user = {'username' : 'john'}
    clas = [
        {
        'author': {'username' : 'islam'},
         'post' : 'flask is the best'
        },
        {
        'author': {'username' : 'john'},
         'post' : 'im in pediforte'
        },
        {
        'author': {'username' : 'sarah'},
         'post' : 'i need ice cream'}
    ]
    return render_template('home.html', name=user, caption='home', clas=clas)


@app.route('/signup')
def sign_up():
    return render_template('signup.html')   


@app.route('/register', methods = ['POST'])
def register():
    username = request.form['username'] 
    email = request.form['email']
    password = request.form['password'] 
    picture = request.files['picture']


    if password == "" or email == "" or password == "":
        flash(" all fields are required! ")
        return redirect (url_for("sign_up"))

    elif len(password) < 6:
        flash("password too short")
        return redirect (url_for("sign_up"))
    else:
        p_hash = hashlib.sha256(password.encode()).hexdigest() 

        print('uploading()'.format(picture.filename))
        #get names of pictures 
        filename = secure_filename(picture.filename)
        #save files
        picture.save(os.path.join(Config.UPLOADS_FOLDER, filename))
        #add form details to db


    existing_user = User.query.filter_by(email=email).first()
    if existing_user == None:
        new_user = User(username=username, email=email, password_hash=p_hash, image=filename)
        db.session.add(new_user)
        db.session.commit()
        flash ('resgistration sucessful')  
        return redirect(url_for('home')) 
    else:
        flash('email already existed') 
    return redirect(url_for('sign_up'))       


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form["username"]
        email = request.form['email']
        password = request.form['password']  
        
        if username == "" or email == "" or password == "":
            flash(" all fields are required! ")
            return redirect (url_for("login"))
        else:
            p_hash = hashlib.sha256(password.encode()).hexdigest()
            #check if the user exist 

            correct_user = User.query.filter_by(email=email).first()
        if correct_user is not None:
            if correct_user.password_hash == p_hash:
                flash('sucessfully logged in ')
                session['email'] = p_hash
                session['p_hash'] = p_hash

                #set cookies
                resp = redirect(url_for('collect'))
                resp.set_cookie('id', str(correct_user.id), max_age=timedelta(hours=24))
                resp.set_cookie('p_hash', p_hash, max_age=timedelta(hours=24))
                return resp
        else:
            flash('invalid login details')
            return redirect(url_for("login"))    
    return render_template("login.html")

@app.route("/logout")
def log_out():
    if "email" in session:
        session.pop("email")
        session.pop("p_hash")
    flash("You have successfully logged out")
    resp = redirect(url_for("login"))
    resp.set_cookie("id", expires=0)
    resp.set_cookie("p_hash", expires=0)
    return resp


@app.route('/collect')
def collect():
    profile = check_login()
    return render_template('collect.html', profile=profile)    

@app.route('/profile') 
def profile():
    profile = check_login()
    print(profile)
    return render_template('profile.html', profile=profile)    


@app.route('/uploads/<filename>')
def view_file(filename):
    return send_from_directory('static/uploads', filename)               
                    






    
