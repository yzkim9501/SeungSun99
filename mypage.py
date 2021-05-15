import pymongo

from flask import Blueprint, render_template, jsonify, request, session, redirect, make_response
import time
import db  # db.py
from auth import login_required

db = db.get_db()
bp = Blueprint('mypage', __name__) #Flask


##게시판 글의 CRUD기능 만들기

## HTML을 주는 부분
@bp.route('/mypage')  # 블루프린트 사용하기! @app.route 대신!
@login_required
def board():
    return render_template('mypage.html')
