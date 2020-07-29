from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging
from functools import wraps
import pymysql
from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.debug=True

db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='myflaskapp')

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/topic')
def topic():
    return render_template('topic.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        id = request.form['email']
        pw = request.form.get('password')
        print([id])
 
        sql='SELECT * FROM users WHERE email = %s'
        cursor  = db.cursor()
        cursor.execute(sql, [id])
        users = cursor.fetchone()
        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                session['is_logged'] = True
                session['username'] = users[3]
                print(session)
                return redirect(url_for('main_page'))
            else:
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


if __name__ =='__main__':
    # ssession 실행시 필요한 설정
    app.secret_key = 'secretKey123456789'
    # 서버 실행
    app.run(host='0.0.0.0', port='8000')