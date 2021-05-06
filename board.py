from flask import Flask, render_template
from flask_cors import CORS, cross_origin

from app import app, db


# HTML 화면 보여주기
@app.route('/board')
@cross_origin()
def board():
    return render_template('board.html')
