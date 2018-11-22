# Decide whether to use SQLAlchemy (ORM) or MySQLdb (Might have to use a fork, MySQLDb does not have good python3 support)
# For now going with pymysql as it is good enough and very similar to MySQLdb
# Please follow the following naming convention: long_function_name(var_one,var_two)
from flask import Flask, flash,session, render_template, request, redirect, Response ,jsonify, json, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from itsdangerous import URLSafeSerializer, BadSignature
import pymysql
import smtplib
import datetime
from ml_1 import reco

COMPANY_EMAIL_ADDRESS = 'alivedead068@gmail.com'
PASSWORD = 'deadoraliveisasecret'

app = Flask(__name__)
app.secret_key = 'totally a secret lolz'
db = pymysql.connect("localhost", "wt2", "pass", "Wt2", charset="latin1")

#To display the home page
@app.route('/')
def index():
    if 's_id' in session:
        return render_template('profile.html', name = session["s_name"])
    return render_template('index.html')

#To validate user form data
@app.route('/validate',methods=['POST'])
def validate():
    data = json.loads(request.data)
    usn = data["usn"]
    email = data["email"]
    pswd = data["password"]

    cursor = db.cursor()
    sql = "SELECT s_id, s_name, s_email, s_password from student where s_id = %s and s_email = %s"
    args = ([usn, email])
    cursor.execute(sql,args)
    results = cursor.fetchall()
    cursor.close()
    print(results)
    if results:
        row = results[0]

        if(row[3] == pswd):
            # do session stuff
            session.clear()
            session['s_id'] = row[0]
            session['s_name'] = row[1]
            return "Correct"
        else:
            # wrong password, tell user
            session.clear()
            return "Wrong"
    # If we still reach here, it means that the user is not a registered one
    return "Missing"

#To display profile page
@app.route('/profile')
def profile():
    if 's_id' in session:
        return render_template('profile.html', name = session["s_name"])
    else:
        return render_template('index.html')

#To retrieve list of courses
@app.route('/getCourses')
def getCourses():
    # print(session)
    try:
        cursor = db.cursor()
        sql = "SELECT c_id, c_name, sem, elective from course where c_id in (select c_id from s_c_map where s_id = %s) and sem=(select max(sem) from course,s_c_map where course.c_id=s_c_map.c_id and s_c_map.s_id=%s);"
        args = ([session['s_id'], session['s_id']])
        cursor.execute(sql,args)
        desc = cursor.description
        results = cursor.fetchall()
        cursor.close()
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in results]
        # print(data)
        session['sem'] = data[0]['sem']-1 
        print(session['sem'])
        return json.dumps(data)
    except pymysql.InternalError as e:
        print(e)
        return None
    

#To retrieve student info
@app.route('/getInfo')
def getInfo():
    # print(session)
    try:
        cursor = db.cursor()
        sql = "SELECT s_id, s_name, s_phone, s_email, (select sum(marks)/(count(marks)*10) from s_c_map where s_id=%s) as s_gpa from student where s_id = %s"
        args = ([session['s_id'], session['s_id']])
        cursor.execute(sql,args)
        desc = cursor.description
        results = cursor.fetchall()
        cursor.close()
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in results]
        # print(data)
        return json.dumps(data)
    except pymysql.InternalError as e:
        print(e)
        return None


#To logout
@app.route('/logout')
def logout():
    if 's_id' in session:
        session.pop('s_id')
        return render_template('index.html')

#To display elective page
@app.route('/elective')
def elective():
    if 's_id' in session:
        return render_template('elective.html', name = session["s_name"])
    else:
        return render_template('index.html')

@app.route('/getElectives')
def getElectives():
    cursor = db.cursor()
    sql = "SELECT c_id from course where elective = 1;"
    # semester = 5;
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    data = [row[0] for row in results]
    details = []
    for x in data:
        details.append(getSubjectDetails(x))
    print('This is being returned by electives: ',details)
    return json.dumps(details)    

def getSubjectDetails(S_Id):
    cursor = db.cursor()
    sql = "SELECT c_id, c_name, sem, pool from course where c_id = %s;"
    cursor.execute(sql,S_Id)
    sub = cursor.fetchall()
    sub1 = list(sub[0])
    column_names = ['c_id','c_name','sem','pool','pre-reqs']
    sql = "SELECT p_id from c_p_map where c_id = %s;"
    cursor.execute(sql,S_Id)
    pre_req = cursor.fetchall()
    pre = [x[0] for x in pre_req]
    sub1.append(pre)
    data = dict(zip(column_names, sub1))
    cursor.close()
    # print(data)
    return data

@app.route('/getElectiveNames/<search_part>')
def getElectiveNames(search_part):
    search_part = search_part+"%";
    column_names = ['c_name'];
    cursor = db.cursor()
    sql = "SELECT c_name from course where elective = 1 AND c_name LIKE %s;"
    cursor.execute(sql,search_part)
    results = cursor.fetchall()
    cursor.close()
    # print(results)
    details = [dict(zip(column_names, row)) for row in results]

    # print(details)
    return json.dumps(details)   



@app.route('/getRecommendation')
def getRecommendation():
    data = reco(session['sem'],session['s_id'])
    print(data) 



    # data = [{'c_id': 'UE15CS334'}, {'c_id': 'UE15CS335'}, {'c_id': 'UE15CS336'},{'c_id': 'UE15CS344'}, {'c_id': 'UE15CS345'}, {'c_id': 'UE15CS346'}]
    return json.dumps(data)


if __name__ == '__main__':
# run!
    app.run(debug=True)








