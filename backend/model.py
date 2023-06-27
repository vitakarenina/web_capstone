from flask import Flask, send_file, request, jsonify, render_template, redirect, url_for, session
from flask_restx import Resource, Api, reqparse

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
api = Api(app, title='API E-Tilang', default='API', default_label='E-Tilang', )

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:''@localhost/db_capstone'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['FOLDER_TILANG'] = 'assets/image/tilang'
app.config['FOLDER_PELANGGARAN'] = "assets/image/pelanggaran"

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy(app)
ma = Marshmallow(app)

##################################### Tabel Tilang ###########################################


class LogTilang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomor_tilang = db.Column(db.String(20), nullable=False)
    no_plat = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    filename_pelanggaran = db.Column(db.String(200), nullable=False)
    pelanggaran = db.Column(db.String(50), nullable=False)
    akurasi = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.DATETIME, nullable=False)

    def __init__(self, nomor_tilang, no_plat, filename, filename_pelanggaran, pelanggaran, akurasi, tanggal):
        self.nomor_tilang = nomor_tilang
        self.no_plat = no_plat
        self.filename = filename
        self.filename_pelanggaran = filename_pelanggaran
        self.pelanggaran = pelanggaran
        self.akurasi = akurasi
        self.tanggal = tanggal


class TilangSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogTilang
        load_instance = True


parser4Param = reqparse.RequestParser()
parser4Param.add_argument('filename', location='files',
                          help='Filename Plat', type=FileStorage, required=True)

parser4Body = reqparse.RequestParser()
parser4Body.add_argument('file', location='files',
                         help='Filename Plat', type=FileStorage, required=True)

################################# Tabel User ###########################################


class LogUsers(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    nomor_plat = db.Column(db.String(100), primary_key=True)
    nomor_bpkb = db.Column(db.String(100), nullable=False)
    pemilik = db.Column(db.String(100), nullable=False)
    jenis_kendaraan = db.Column(db.String(100), nullable=False)
    merk = db.Column(db.String(100), nullable=False)
    warna = db.Column(db.String(20), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    telp = db.Column(db.String(200), nullable=False)

    def __init__(self, nomor_plat, nomor_bpkb, pemilik, jenis_kendaraan, merk, warna, alamat, email, telp):
        self.nomor_plat = nomor_plat
        self.nomor_bpkb = nomor_bpkb
        self.pemilik = pemilik
        self.jenis_kendaraan = jenis_kendaraan
        self.merk = merk
        self.warna = warna
        self.alamat = alamat
        self.email = email
        self.telp = telp


class SchemaUsers(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogUsers
        load_instance = True


parserParamUsers = reqparse.RequestParser()
parserParamUsers.add_argument(
    'nomor_plat', type=str, help='Masukan Nomor Plat', location='args')
parserParamUsers.add_argument(
    'pemilik', type=str, help='Masukan Nama Pemilik', location='args')
parserParamUsers.add_argument(
    'nomor_bpkb', type=str, help='Masukan Nomor BPKB', location='args')
parserParamUsers.add_argument(
    'jenis_kendaraan', type=str, help='Masukan Jenis Kendaraan', location='args')
parserParamUsers.add_argument(
    'merk', type=str, help='Masukan Merk Kendaraan', location='args')
parserParamUsers.add_argument(
    'warna', type=str, help='Masukan Warna Kendaraan', location='args')
parserParamUsers.add_argument(
    'alamat', type=str, help='Masukan Alamat Pemilik', location='args')
parserParamUsers.add_argument(
    'email', type=str, help='Masukan Email Pemilik', location='args')
parserParamUsers.add_argument(
    'telp', type=str, help='Masukan No Telp Pemilik', location='args')

parserBodyUsers = reqparse.RequestParser()
parserBodyUsers.add_argument(
    'nomor_plat', type=str, help='Masukan Nomor Plat', location='args')
parserBodyUsers.add_argument(
    'pemilik', type=str, help='Masukan Nama Pemilik', location='args')
parserBodyUsers.add_argument(
    'nomor_bpkb', type=str, help='Masukan Nomor BPKB', location='args')
parserBodyUsers.add_argument(
    'jenis_kendaraan', type=str, help='Masukan Jenis Kendaraan', location='args')
parserBodyUsers.add_argument(
    'merk', type=str, help='Masukan Merk Kendaraan', location='args')
parserBodyUsers.add_argument(
    'warna', type=str, help='Masukan Warna Kendaraan', location='args')
parserBodyUsers.add_argument(
    'alamat', type=str, help='Masukan Alamat Pemilik', location='args')
parserBodyUsers.add_argument(
    'email', type=str, help='Masukan Email Pemilik', location='args')
parserBodyUsers.add_argument(
    'telp', type=str, help='Masukan No Telp Pemilik', location='args')


############### Tabel Admin ################


class LogAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        # self.tanggal = tanggal


class SchemaAdmin(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LogAdmin
        load_instance = True


parserParamAdmin = reqparse.RequestParser()
parserParamAdmin.add_argument(
    'username', type=str, help='Masukan Username Admin', location='args')
parserParamAdmin.add_argument(
    'email', type=str, help='Masukan Email Admin', location='args')
parserParamAdmin.add_argument(
    'password', type=str, help='Masukan Password Admin', location='args')

parserBodyAdmin = reqparse.RequestParser()
parserBodyAdmin.add_argument(
    'username', type=str, help='Masukan Username Admin', location='args')
parserBodyAdmin.add_argument(
    'email', type=str, help='Masukan Email Admin', location='args')
parserBodyAdmin.add_argument(
    'password', type=str, help='Masukan Password Admin', location='args')
