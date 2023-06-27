from backend.model import db, app, api, LogUsers, parserParamUsers, parserBodyUsers, SchemaUsers, LogAdmin, SchemaAdmin, parserBodyAdmin, parserParamAdmin
from flask import Flask, send_file, request, jsonify, render_template, redirect, url_for, session
from flask_restx import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash
from datetime import datetime
from backend.backend import app, mysql
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash


@app.route("/api/create_user", methods=["GET"])
def users_db():
    with app.app_context():
        db.create_all()
        return "Database User Telah dibuat" + ' <a href="/"> Kembali</a>'


@app.route("/api/create_admin", methods=["GET"])
def admin_db():
    with app.app_context():
        db.create_all()
        return "Database Admin Telah dibuat" + ' <a href="/"> Kembali</a>'

# @app.route("/user/flutter", methods=["GET"])
# def getAllUsers():
#     history = LogUsers.query.all()
#     users_schema = SchemaUsers(many=True)
#     output = users_schema.dump(history)
#     return jsonify({'users': output})

############################### USER ########################################


@api.route('/api/user', methods=["GET", "POST"])
class UserAPI(Resource):
    def get(self):
        log_data = db.session.execute(
            db.select(LogUsers.nomor_plat, LogUsers.nomor_bpkb, LogUsers.pemilik, LogUsers.jenis_kendaraan, LogUsers.merk, LogUsers.warna, LogUsers.alamat)).all()
        if (log_data is None):
            return f"Tidak Ada Data User!"
        else:
            data = []
            for user in log_data:
                data.append({
                    # 'id': user.id,
                    'nomor_plat': user.nomor_plat,
                    'nomor_bpkb': user.nomor_bpkb,
                    'pemilik': user.pemilik,
                    'jenis_kendaraan': user.jenis_kendaraan,
                    'merk': user.merk,
                    'warna': user.warna,
                    'alamat': user.alamat,
                })
            return data

    @api.expect(parserBodyUsers)
    def post(self):
        d = {}
        if request.method == "POST":
            args = parserBodyUsers.parse_args()
            nomor_plat = args["nomor_plat"]
            nomor_bpkb = args["nomor_bpkb"]
            pemilik = args["pemilik"]
            jenis_kendaraan = args["jenis_kendaraan"]
            merk = args["merk"]
            warna = args["warna"]
            alamat = args["alamat"]

            var_bpkb = LogUsers.query.filter_by(nomor_bpkb=nomor_bpkb).first()

            if var_bpkb is None:
                register = LogUsers(nomor_plat=nomor_plat, nomor_bpkb=nomor_bpkb,
                                    pemilik=pemilik, jenis_kendaraan=jenis_kendaraan, merk=merk, warna=warna, alamat=alamat)

                db.session.add(register)
                db.session.commit()

                return jsonify(["Register User success"])
            else:
                return jsonify(["Data User Sudah Terdaftar"])

# Delete Image


@api.route('/user/<string:nomor_bpkb>')
class UserAPI(Resource):
    def delete(self, nomor_bpkb):
        users = db.session.execute(
            db.select(LogUsers).filter_by(nomor_bpkb=nomor_bpkb)).first()
        if (users is None):
            return f"Data User dengan Nomor BPKB {nomor_bpkb} tidak ditemukan!"
        else:
            tilang = users[0]
            db.session.delete(tilang)
            db.session.commit()
            return f"Data User dengan Nomor BPKB {nomor_bpkb} berhasil dihapus!"


############################### ADMIN ########################################

@api.route('/api/admin', methods=["GET", "POST"])
class AdminAPI(Resource):
    def get(self):
        log_data = db.session.execute(
            db.select(LogAdmin.id, LogAdmin.username, LogAdmin.email, LogAdmin.password)).all()
        if (log_data is None):
            return f"Tidak Ada Data Admin!"
        else:
            data = []
            for admin in log_data:
                data.append({
                    'id': admin.id,
                    'username': admin.username,
                    'email': admin.email,
                    'password': admin.password
                })
            return data

    @api.expect(parserBodyAdmin)
    def post(self):
        d = {}
        if request.method == "POST":
            args = parserBodyAdmin.parse_args()
            username = args["username"]
            mail = args["email"]
            password = args["password"]

            email = LogAdmin.query.filter_by(email=mail).first()

            if email is None:
                register_admin = LogAdmin(username=username,
                                          email=mail, password=password)

                db.session.add(register_admin)
                db.session.commit()

                return jsonify(["Register Admin success"])
            else:
                return jsonify(["Data Admin Sudah Terdaftar"])

# Flutter


@app.route('/api/register', methods=["GET", "POST"])
def flutter_register():
    d = {}
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

        reg_bpkb = LogUsers.query.filter_by(nomor_bpkb=nomor_bpkb).first()

        if reg_bpkb is None:
            register = LogUsers(nomor_plat=nomor_plat, nomor_bpkb=nomor_bpkb,
                                pemilik=pemilik, jenis_kendaraan=jenis_kendaraan, merk=merk, warna=warna, alamat=alamat, email=email, telp=telp)

            db.session.add(register)
            db.session.commit()

            return jsonify(["Register success, Silahkan Login!"])
        else:
            # already exist

            return jsonify(["Username Sudah Ada, Cek Ulang!"])


@app.route('/api/login', methods=["GET", "POST"])
def flutter_login():
    d = {}
    if request.method == "POST":
        nomor_plat = request.form["nomor_plat"]
        nomor_bpkb = request.form["nomor_bpkb"]

        var_bpkb = LogUsers.query.filter_by(
            nomor_plat=nomor_plat, nomor_bpkb=nomor_bpkb).first()

        if var_bpkb is None:
            # acount not found
            return jsonify(["Nomor BPKB Tidak Terdaftar!"])
        else:
            # acount found
            return jsonify(["Login Success, Selamat Datang!"])
