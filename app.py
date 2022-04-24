import re
from unittest import result
from click import password_option
from flask import Flask, render_template, request_finished, session, request, url_for, redirect, flash
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.secret_key = '!@#$%'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coba-crud'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    cur = mysql.connection.cursor()
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pengguna where username=%s and password=%s", (username, password))
        result = cur.fetchone()
        if result:
            # jika login valid buat data sesion
            session['is_logged_in'] = True
            session['username'] = result[1]
            # Redirect ke halaman home
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pengguna order by nim")
        data = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', row=data)
    else:
        return redirect(url_for("login"))





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        nim = request.form['nim']
        nama = request.form['nama']
        prodi = request.form['prodi']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        username = request.form['username']
        password = request.form['password']
    
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pengguna (nim, nama, prodi, jenis_kelamin, alamat, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nim, nama, prodi, jenis_kelamin, alamat, username, password))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('login'))

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "GET":
        return render_template('insert.html')
    else:
        nim = request.form['nim']
        nama = request.form['nama']
        prodi = request.form['prodi']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        username = request.form['username']
        password = request.form['password']
    

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pengguna (nim, nama, prodi, jenis_kelamin, alamat, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nim, nama, prodi, jenis_kelamin, alamat, username, password))
        mysql.connection.commit()
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('dashboard'))


@app.route('/delete/<string:nim>', methods=['GET'])
def delete(nim):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pengguna WHERE nim = {}".format(nim)) 
    mysql.connection.commit()
    return redirect(url_for('dashboard'))



@app.route('/update', methods=["GET", "POST"])
def update():
    nim = request.form['nim']
    nama = request.form['nama']
    prodi = request.form['prodi']
    jenis_kelamin = request.form['jenis_kelamin']
    alamat = request.form['alamat']
    sql = "UPDATE pengguna SET nama=%s, prodi=%s, jenis_kelamin=%s, alamat=%s WHERE nim=%s"
    data = (nama, prodi, jenis_kelamin, alamat, nim)
    cur = mysql.connection.cursor()
    cur.execute(sql, data)
    mysql.connection.commit()
    flash('User updated successfully!')
    return redirect(url_for('dashboard'))


    # route logout
@app.route('/logout')
def logout():
    session.pop('is_logged_in')
    session.pop('username', None)
    return redirect(url_for('login'))


# debug and auto reload
if __name__ == '__main__':
    app.run(debug=True, port=8000)