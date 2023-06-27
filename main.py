from backend.model import app, db, ma
from flask import Flask, render_template, request, jsonify
from backend.API import tilang
from backend import backend
from backend.backend import login, dashboard, surat, logout, tilang, users_form, add_user, landing, live, video, live_page, generate_frames, delete_tilang, video_testing, admin_form, add_admin, ketentuan
from chatbot.chat import chatbot_response, getResponse, get_bot_response, words, home, np, bow, lemmatizer, intents, classes, predict_class, WordNetLemmatizer, clean_up_sentence, model, load_model

from backend.API.users import flutter_register, flutter_login, UserAPI, AdminAPI, admin_db, users_db


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == '__main__':
    # app.run(host='192.168.208.106', debug=True, port=5000)
    app.run(debug=True)
