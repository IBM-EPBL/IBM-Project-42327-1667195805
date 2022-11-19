from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import os



app = Flask(__name__)
  
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=8e359033-a1c9-4643-82ef-8ac06f5107eb.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30120;Security=SSL;UID=cht63408;PWD=OZRWkZZcuxUb5In9;PROTOCOL=TCPIP",'', '')

@app.route('/')    
def login():
    return render_template('login.html')


@app.route('/login',methods=['GET', 'POST'])
def loginpage():
    global userid
    msg = ''

    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT uname FROM register WHERE uname =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            return redirect(url_for('dash'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  if __name__ == '__main__':
   app.run(host='0.0.0.0',debug='TRUE')
