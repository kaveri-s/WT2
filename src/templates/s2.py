
from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itsdangerous import URLSafeSerializer, BadSignature
import pymysql
import smtplib
import datetime

COMPANY_EMAIL_ADDRESS = 'alivedead068@gmail.com'
PASSWORD = 'deadoraliveisasecret'
app = Flask(__name__)
app.secret_key = 'totally a secret lolz'
# db = pymysql.connect("localhost", "wt2", "pass",charset="latin1")
# # cursor = db.cursor()
# db.cursor().execute('create database WT2')


@app.route('/')
def index():
    '''This function renders the index page of the EventManagement site'''
    print(request.method)
    return render_template('index.html')

@app.route('/profile')
def profile():
    '''This function renders the index page of the EventManagement site'''
    print(request.method)
    return render_template('profile.html')

@app.route('/elective')
def elective():
    '''This function renders the index page of the EventManagement site'''
    print(request.method)
    return render_template('elective.html')

if __name__ == '__main__':
# run!
    app.run(debug=True)
