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


# def data_for_monitor(f):
#     @wraps(f)
#     def wrap(*args , **kwargs):
#         cursor = db.cursor()
#         sql='SELECT * FROM solar_{};'.format(session['id'])
#         cursor.execute(sql)
#         data = cursor.fetchall()
#         print(data)
#         return data 
#     return wrap


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
                session['id'] = users[0]
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

@app.route('/register', methods=['POST','GET'])
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
        sql = "SELECT username FROM users WHERE username =%s"
        cursor.execute(sql,[username])
        exist  = cursor.fetchone()
        if exist :
            return redirect(url_for('register'))
        else:
            if(pbkdf2_sha256.verify(re_password,password)):

                sql = '''
                    INSERT INTO users (name , email , username , password) 
                    VALUES (%s ,%s, %s, %s)
                '''
                cursor.execute(sql , (name,email,username,password))
                db.commit()

                sql_find_Serial_num = "SELECT id FROM users WHERE username =%s"
                cursor.execute(sql_find_Serial_num,[username])
                db.commit()
                sol_num = cursor.fetchone()
                print(int(sol_num[0]))

                sql_for_newtable = '''
                    CREATE TABLE `myflaskapp`.`solar_%s` (
                    `data_num` INT NOT NULL AUTO_INCREMENT,
                    `Lux` INT NULL,
                    `Temp` INT NULL,
                    `Humid` INT NULL,
                    `Time` DATETIME NULL,
                    PRIMARY KEY (`data_num`));
                '''
                cursor.execute(sql_for_newtable,[int(sol_num[0])])
                db.commit()
                return redirect(url_for('login'))
            else:
                return "Invalid Password"
        db.close()
    else:
        return render_template('register.html')


@app.route('/monitor')
# @data_for_monitor
def monitor():
    cursor = db.cursor()
    sql='SELECT * FROM solar_{};'.format(session['id'])
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('monitor.html', m_data= data)
@app.route('/monitor1')
# @data_for_monitor
def monitor1():
    cursor = db.cursor()
    sql='SELECT * FROM solar_{};'.format(session['id'])
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('monitor1.html',m_data= data)
@app.route('/monitor2')
# @data_for_monitor
def monitor2():
    cursor = db.cursor()
    sql='SELECT * FROM solar_{};'.format(session['id'])
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('monitor2.html',m_data= data)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')


if __name__ =='__main__':
    # ssession 실행시 필요한 설정
    app.secret_key = 'secretKey123456789'
    # 서버 실행
    app.run(host='0.0.0.0', port='8000')