# import module
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime

#from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#from werkzeug.security import generate_password_hash, check_password_hash

#import users_dao, workout_dao

from models import Aula, Professore, Richiesta, Slot

from datetime import datetime



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
