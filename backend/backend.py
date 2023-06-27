import time
from backend.model import db, app, allowed_file, LogTilang, LogUsers, LogAdmin
from flask import Flask, send_file, request, jsonify, render_template, redirect, url_for, session, Response
from werkzeug.security import generate_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import pytesseract
import cv2
import os
import numpy as np
from keras.models import load_model

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash

# app = Flask(__name__)

app.secret_key = '$capsTone_pRoject_'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_capstone'

mysql = MySQL(app)

def frame_video():
    # Load the model
    model = load_model(
        'E:/CAPSTONE/web_capstone/assets/model_tilang/keras_model.h5')

    # CAMERA can be 0 or 1 based on default camera of your computer.
    video = cv2.VideoCapture(
        'E:/CAPSTONE/web_capstone/assets/testing.mp4')

    # Grab the labels from the labels.txt file. This will be used later.
    labels = open(
        'E:/CAPSTONE/web_capstone/assets/model_tilang/labels.txt', 'r').readlines()

    deteksi = cv2.CascadeClassifier("assets/model_tilang/haarcascade_russian_plate_number.xml")

    # classifier
    minArea = 500

    i = 0

    while (video.isOpened()):
        # Grab the webcameras image.

        ret, img = video.read()

        text = ""

        if ret == True:
            np.set_printoptions(suppress=True)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # img = cv2.resize(img, (224, 224))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            helm = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

            image = cv2.resize(helm, (224, 224), interpolation=cv2.INTER_AREA)
            # turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            data[0] = normalized_image_array

            prediction = model.predict(data)
            print(prediction)

            tanggal = datetime.now()
            tanggal_baru = tanggal.strftime('%Y-%m-%d %H:%M:%S')

            for i in prediction:
                if i[0] > 0.75:
                    text = "Pakai Helm"
                if i[1] > 0.75:
                    text = "Tanpa Helm"

                    a = 0
                    b = a + 1
                    filename = "assets/image/tilang/Pelanggaran-" + str(b) + ".png"
                    cut1 = img[:, :]
                    cv2.imwrite(filename, cut1)
                    print(filename)
                    # cv2.imshow(filename,cut1)
                    # time.sleep(10)
                    # if a == 3:
                    #     time.sleep(30)
                    #     a = 0

                print(text)
                # desc = text + ' : ' + str(prediction)
                img = cv2.resize(img, (500, 500))
                cv2.putText(img, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

            # Detect plate number using HAAR Cascade
            # plates = deteksi.detectMultiScale(gray, 1.3, 5)
            #
            # for (x, y, w, h) in plates:
            #     area = w * h
            #     if area > minArea:
            #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #         cv2.putText(img, "PlatNomor", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            #         roi_gray = gray[y:y + h, x:x + w]
            #         cv2.imshow("IMG", roi_gray)
            #         i = i + 1
            #         filename = 'assets/image/tilang/plat/Gambar Plat-' + str(i) + '.png'
            #         cv2.imwrite(filename, roi_gray)
            #         time.sleep(1)
            #         if i < 4:
            #             # Menggunakan pytesseract untuk mendeteksi plat motor dari gambar
            #             pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
            #             text = pytesseract.image_to_string(filename)
            #             capture_time = datetime.datetime.now()
            #             print(capture_time, text)
            #
            #             # Menyimpan data plat motor ke tabel MySQL
            #             # query = "INSERT INTO log_parkir (no_plat, tanggal) VALUES (%s, %s)"
            #             # cursor.execute(query, (text, capture_time))
            #             # cnx.commit()
            #             # time.sleep(1)
            #         else:
            #             time.sleep(60)
            #             i - 0

            frame = cv2.imencode('.jpg', img)[1]
            encode = frame.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + encode + b'\r\n')
            time.sleep(0.1)
        else:
            break


def generate_frames():
    model = load_model(
        'E:/CAPSTONE/web_capstone/assets/model_tilang/keras_model.h5')

    # CAMERA can be 0 or 1 based on default camera of your computer.
    video = cv2.VideoCapture('http://10.236.248.181:8080/video')

    # Grab the labels from the labels.txt file. This will be used later.
    labels = open(
        'E:/CAPSTONE/web_capstone/assets/model_tilang/labels.txt', 'r').readlines()

    # deteksi = cv2.CascadeClassifier("assets/model_tilang/haarcascade_russian_plate_number.xml")

    # classifier
    minArea = 500

    i = 0

    while (video.isOpened()):
        # Grab the webcameras image.

        ret, img = video.read()

        text = ""

        if ret == True:
            np.set_printoptions(suppress=True)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

            # img = cv2.resize(img, (224, 224))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            helm = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)

            image = cv2.resize(helm, (224, 224), interpolation=cv2.INTER_AREA)
            # turn the image into a numpy array
            image_array = np.asarray(image)

            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

            data[0] = normalized_image_array

            prediction = model.predict(data)
            print(prediction)
            for i in prediction:
                if i[1] > 0.65:
                    text = "Pakai Helm"
                if i[0] > 0.65:
                    text = "Tidak Pakai Helm"

                    a = 0
                    b = a + 1
                    filename = "assets/image/tilang/Live-" + str(b) + ".png"
                    cut1 = img[:, :]
                    cv2.imwrite(filename, cut1)
                    print(filename)
                    #             cv2.imshow(filename,cut1)
                    # time.sleep(10)
                    # if a == 3:
                    #     time.sleep(30)
                    #     a = 0

                print(text)
                # desc = text + ' : ' + str(prediction)
                img = cv2.resize(img, (500, 500))
                cv2.putText(img, text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

            # Detect plate number using HAAR Cascade
            # plates = deteksi.detectMultiScale(gray, 1.3, 5)
            #
            # for (x, y, w, h) in plates:
            #     area = w * h
            #     if area > minArea:
            #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #         cv2.putText(img, "PlatNomor", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            #         roi_gray = gray[y:y + h, x:x + w]
            #         cv2.imshow("IMG", roi_gray)
            #         i = i + 1
            #         filename = 'assets/image/tilang/plat/Gambar Plat-' + str(i) + '.png'
            #         cv2.imwrite(filename, roi_gray)
            #         time.sleep(1)
            #         if i < 4:
            #             # Menggunakan pytesseract untuk mendeteksi plat motor dari gambar
            #             pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
            #             text = pytesseract.image_to_string(filename)
            #             capture_time = datetime.datetime.now()
            #             print(capture_time, text)
            #
            #             # Menyimpan data plat motor ke tabel MySQL
            #             # query = "INSERT INTO log_parkir (no_plat, tanggal) VALUES (%s, %s)"
            #             # cursor.execute(query, (text, capture_time))
            #             # cnx.commit()
            #             # time.sleep(1)
            #         else:
            #             time.sleep(60)
            #             i - 0

            frame = cv2.imencode('.jpg', img)[1]
            encode = frame.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + encode + b'\r\n')
            time.sleep(0.1)
        else:
            break


@app.route('/live')
def live():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Load Live


@app.route('/live_page')
def live_page():
    return render_template("tampilan/video/live.html")

# Load Video


@app.route('/video')
def video():
    return Response(frame_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# routing
@app.route('/video_testing')
def video_testing():
    return render_template("tampilan/video/video.html")


# User
# Delete


@app.route('/delete_user/<int:nomor_plat>', methods=['GET'])
def delete_user(nomor_plat):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE 
            FROM log_users
            WHERE nomor_plat=%s''', (nomor_plat,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('users_form'))

    return render_template('tampilan/users/user.html')

# Get


@app.route('/users_form', methods=['GET', 'POST'])
def users_form():
    if request.method == "GET":
        us = LogUsers.query.all()
        return render_template("tampilan/users/user.html", user=us)

# Add


@app.route("/add_user", methods=('GET', 'POST'))
def add_user():
    # msg = ''
    if request.method == "POST":
        nomor_plat = request.form["nomor_plat"]
        nomor_bpkb = request.form["nomor_bpkb"]
        pemilik = request.form["pemilik"]
        jenis_kendaraan = request.form["jenis_kendaraan"]
        merk = request.form["merk"]
        warna = request.form["warna"]
        alamat = request.form["alamat"]
        email = request.form["email"]
        telp = request.form["telp"]

        var_bpkb = LogUsers.query.filter_by(nomor_bpkb=nomor_bpkb).first()

        if var_bpkb is None:
            register = LogUsers(nomor_plat=nomor_plat, nomor_bpkb=nomor_bpkb,
                                pemilik=pemilik, jenis_kendaraan=jenis_kendaraan, merk=merk, warna=warna, alamat=alamat, email=email, telp=telp)

            db.session.add(register)
            db.session.commit()

            return redirect(url_for('users_form'))
        else:
            return redirect(url_for('users_form'))
    return render_template('tampilan/users/tambah_user.html')

# Admin
# Delete


@app.route('/delete_admin/<int:id>', methods=['GET'])
def delete_admin(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE 
            FROM log_admin 
            WHERE id=%s''', (id,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin_form'))

    return render_template('tampilan/users/admin.html')

# Get Data


@app.route('/admin_form', methods=['GET', 'POST'])
def admin_form():
    if request.method == "GET":
        us = LogAdmin.query.all()
        return render_template("tampilan/users/admin.html", user=us)

# Add Data


@app.route("/add_admin", methods=('GET', 'POST'))
def add_admin():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # tanggal = request.form['tanggal']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM log_users WHERE username = % s', (username, ))
        log_users = cursor.fetchone()
        if log_users:
            msg = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute(
                'INSERT INTO log_admin VALUES (NULL, % s, % s, % s)', (username,  email, password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return redirect(url_for('admin_form'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('tampilan/users/admin.html', msg=msg)


# Function Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM log_admin WHERE username = % s AND password = % s', (username, password, ))
        log_users = cursor.fetchone()
        if log_users:
            session['loggedin'] = True
            session['id'] = log_users['id']
            session['username'] = log_users['username']
            msg = 'logged in successfully !'
            return redirect(url_for('dashboard', msg=msg))
        else:
            msg = 'Username dan Password tidak cocok!'
    return render_template('tampilan/login/login.html', msg=msg)

# Load Dasbor


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # session.pop('loggedin', None)
    return render_template("tampilan/dasbor/dashboard.html")

#  Logout


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# Template Tilang


@app.route('/tilang', methods=['GET', 'POST'])
def tilang():
    if request.method == "GET":
        rv = LogTilang.query.all()
        return render_template("tampilan/tilang/data.html", tilang=rv)

# Delet Data Tilang


@app.route('/delete_tilang/<int:id>', methods=['GET'])
def delete_tilang(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''
            DELETE 
            FROM log_tilang 
            WHERE id=%s''', (id,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('tilang'))

    return render_template('tampilan/tilang/data.html')

# Template Upload


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template("tampilan/upload/upload.html")

# Landing Page


@app.route('/landing', methods=['GET', 'POST'])
def landing():
    return render_template("tampilan/landing/landing-page.html")


@app.route('/ketentuan', methods=['GET', 'POST'])
def ketentuan():
    return render_template("tampilan/landing/landing-page.html")

# Surat Tilang


@app.route('/surat', methods=['GET', 'POST'])
def surat():
    return render_template("tampilan/surat/surat_tilang.html")
