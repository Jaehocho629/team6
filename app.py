from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging

import pymysql
from passlib.hash import pbkdf2_sha256
from data import Articles
from functools import wraps

app = Flask(__name__)
app.debug=True
app.secret_key = "super secret key"

db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='team6')

def is_logged_out(f):
    @wraps(f)
    def wrap(*args , **kwargs):
        if 'is_logged' in session:
        # if is session['is_logged']:
            return redirect(url_for('articles'))
        else:
            return f(*args ,**kwargs)
    return wrap

def is_logged_in(f):
    @wraps(f)
    def _wraper(*args, **kwargs):
        if 'is_logged' in session:#아래와 같은말임
        # if session['is_logged']:#위와 같은 말임
            return f(*args, **kwargs)
        else:
            flash('UnAuthorized, Please login', 'dnager')
            return redirect(url_for('login'))
    return _wraper


@app.route('/')
@is_logged_in
def index():
    print("Success")
    # session['test'] = "Hokyoung Kim"
    # session_data = session
    # print(session_data)
    # # return "TEST"
    return render_template('home.html')


@app.route('/register',methods=['GET' ,'POST'])
@is_logged_out
def register():
    if request.method == 'POST':

        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        # name = form.name.data

        cursor = db.cursor()
        sql = 'SELECT username FROM users WHERE username = %s'
        cursor.execute(sql,[username])
        username_one = cursor.fetchone()

        if  username_one :
            return redirect(url_for('register'))
        else:

            if(pbkdf2_sha256.verify(re_password,password )):
                print(pbkdf2_sha256.verify(re_password,password ))
            
                sql = '''
                    INSERT INTO users (name , email , username , password) 
                    VALUES (%s ,%s, %s, %s )
                '''
                cursor.execute(sql , (name,email,username,password ))
                db.commit()
            

                # cursor = db.cursor()
                # cursor.execute('SELECT * FROM users;')
                # users = cursor.fetchall()
            
                return redirect(url_for('login'))

            else:
                return redirect(url_for('register'))

        db.close()
    else:
        return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
@is_logged_out
def login():
    if request.method == 'POST':
        id = request.form['username']
        pw = request.form.get('password')
        print([id])

        sql='SELECT * FROM users WHERE username = %s'
        cursor  = db.cursor()
        cursor.execute(sql, [id])
        users = cursor.fetchone()
        print(users)

        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                session['is_logged'] = True
                session['username'] = users[3]
                session['id'] = users[0]
                print(session)
                return redirect('/')
            else:
                return redirect(url_for('login'))
        
    else:
        return render_template('login.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/graph')
@is_logged_in
def graph():
    list_data = [5, 10, 15, 40, 50, 15, 10,5,40]
    return render_template('graph.html',data = list_data)

@app.route('/delete/<string:id>',methods = ['POST'])
@is_logged_in
def delete(id):
   cursur = db.cursor()
   sql = 'DELETE FROM `users` WHERE  `id`=%s;'
   session.clear()
   cursur.execute(sql,[id])
   db.commit()
   return redirect('/')



if __name__ =='__main__':
    app.run(host='0.0.0.0', port='8000')
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.secret_key = 'hokyoung123456789'# ssession 실행시 필요한 설정이다
    app.run() # 서버 실행