from backend.model import db, app, api, LogTilang, TilangSchema, parser4Param, parser4Body
from flask import Flask, send_file, request, jsonify, render_template, redirect, url_for, session
from flask_restx import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from datetime import datetime
import pytesseract
import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from keras.models import load_model
from PIL import Image, ImageOps  # Install pillow instead of PIL
import imutils
import argparse
import uuid
# from geopy.geocoders import Nominatim

# create db tilang


@app.route("/api/create_image", methods=["GET"])
def create_db():
    with app.app_context():
        db.create_all()
        return "Database Telah dibuat" + ' <a href="/"> Kembali</a>'

# get for mobile apps


# @app.route("/api/flutter", methods=["GET"])
# def getAllTilang():
#     history = LogTilang.query.all()
#     tilang_schema = TilangSchema(many=True)
#     output = tilang_schema.dump(history)
#     return jsonify({'tilang': output})


@api.route('/api/tilang')
class TilangAPI(Resource):
    def get(self):
        log_data = db.session.execute(
            db.select(LogTilang.id, LogTilang.no_plat,
                      LogTilang.pelanggaran, LogTilang.akurasi, LogTilang.tanggal)).all()
        if (log_data is None):
            return f"Tidak Ada Data Tilang!"
        else:
            data = []
            for history in log_data:
                data.append({
                    'id': history.id,
                    'no_plat': history.no_plat,
                    # 'filename': history.filename,
                    # 'filename_pelanggaran': history.filename_pelanggaran,
                    'pelanggaran': history.pelanggaran,
                    'akurasi': history.akurasi,
                    'tanggal': history.tanggal.strftime('%Y-%m-%d %H:%M:%S')
                })
            return data

    @api.expect(parser4Body)
    def post(self):
        # global no_plat
        katTilang = "TLG-HELM"

        k = uuid.uuid4()
        # kodeTilang = k + 1
        tlg = katTilang + "-" + str(k)
        nomor_tilang = tlg

        args = parser4Body.parse_args()
        # Plat
        file = args['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['FOLDER_TILANG'], filename))

        foto = cv2.imread(
            "E:/CAPSTONE/web_capstone/assets/image/tilang/" + file.filename)
        # img = cv2.imread(foto)

        image = imutils.resize(foto, width=300)
        # shape = image.shape[:2]
        # blob = cv2.dnn.blobFromImage(shape, 0.007843, (300, 300), 127.5)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
        edged = cv2.Canny(gray_image, 30, 200)

        cnts, new = cv2.findContours(
            edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image1 = image.copy()
        cv2.drawContours(image1, cnts, -1, (0, 255, 0), 1)

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        screenCnt = None
        image2 = image.copy()
        cv2.drawContours(image2, cnts, -1, (0, 255, 0), 2)

        i = 0
        b = i + 1
        path = 'E:/CAPSTONE/web_capstone/assets/image/tilang/plat/'
        name = 'image-' + str(b) + '.jpg'
        simpan = path + name

        screenCnt = None
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx
                x, y, w, h = cv2.boundingRect(c)
                new_img = image[y:y + h, x:x + w]
                cv2.imwrite(simpan, new_img)
                i += 1
                break

        cv2.drawContours(image, [screenCnt],  0, 255, -1,)
        filename_ = simpan

        reader = easyocr.Reader(['en'])
        result = reader.readtext(filename_)

        # Output
        for i in range(len(result) - 1):
            plat = result[i][1]

        no_plat = result[i][1]
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
        # i = 0
        # klasifikasi = cv2.CascadeClassifier(
        #         'E:/CAPSTONE/web_capstone/assets/model_tilang/indian_license_plate.xml')

        # pelanggaran
        np.set_printoptions(suppress=True)
        model = load_model(
            'E:/CAPSTONE/web_capstone/assets/model_tilang/keras_model.h5', compile=False)
        class_names = open(
            'E:/CAPSTONE/web_capstone/assets/model_tilang/labels.txt').readlines()

        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        fotopelanggaran = Image.open(
            "E:/CAPSTONE/web_capstone/assets/image/tilang/" + file.filename).convert('RGB')

        size = (224, 224)
        image = ImageOps.fit(fotopelanggaran, size, Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        index = np.argmax(prediction)
        # pelanggaran = class_names[index]
        confidence_score = prediction[0][index]
        akurasi = confidence_score * 100 #0,9999*100 = 99,..%

        # print("Nomor Plat : " + no_plat)
        # print("Pelanggaran : " + pelanggaran)

        # tanggal
        tanggal = datetime.now()
        tanggal_baru = tanggal.strftime('%Y-%m-%d %H:%M:%S')

        for i in prediction:
            if i[0] > 0.75:
                pelanggaran = "Tidak Pakai Helm"
                tilang = LogTilang(
                    nomor_tilang=nomor_tilang,
                    no_plat=no_plat,
                    filename=filename_,
                    filename_pelanggaran=filename_,
                    pelanggaran=pelanggaran,
                    akurasi=round(akurasi, 3),
                    tanggal=tanggal_baru,
                )
                db.session.add(tilang)
                db.session.commit()

            if i[1] > 0.75:
                pelanggaran = "Pakai Helm"
                return {'message': f"Gambar ini memakai helm!!!"}

        return {
            # 'Nomor Tilang': nomor_tilang,
            'Nomor Plat': no_plat,
            'Pelanggaran': pelanggaran,
            # 'Akurasi Pelanggaran': round(akurasi, 2),
            'Tanggal': tanggal_baru,
            # 'status'     : 200,
            'message_true': f"Data dengan nomor {no_plat} berhasil masuk!"
        }


# Delete
@api.route('/api/<string:no_plat>')
class TilangAPI(Resource):
    def delete(self, no_plat):
        tilangs = db.session.execute(
            db.select(LogTilang).filter_by(no_plat=no_plat)).first()
        if (tilangs is None):
            return f"Data Tilang dengan Nomor Plat {no_plat} tidak ditemukan!"
        else:
            tilang = tilangs[0]
            db.session.delete(tilang)
            db.session.commit()
            return f"Data Tilang dengan Nomor Plat {no_plat} berhasil dihapus!"
