from flask import Flask, render_template
from flask_cors import CORS, cross_origin

from app import app, db


# HTML 화면 보여주기
@app.route('/study')
@cross_origin()
def study():
    return render_template('study.html')
