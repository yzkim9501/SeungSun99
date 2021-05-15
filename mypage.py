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



@bp.route('/api/view_mystudy', methods=['GET'])
@login_required
def view_mystudy():

    if request.method == "GET":

        my_id=session['user_id']


        datas = list(db.join_member.find({'user_id': my_id}))  # _id로 스터디 도큐먼트 검색.
        my_study_idxs=[]
        for data in datas:
            my_study_idxs.append(data['study_index'])

        datas = list(db.study.find({'leader_id': my_id}))  # _id로 스터디 도큐먼트 검색.
        for data in datas:
            my_study_idxs.append(data['_id'])

        return jsonify(list(db.study.find({'_id':{ '$in' : my_study_idxs}})))


@bp.route('/api/view_joinmember', methods=['GET'])
@login_required
def view_joinmember():

    if request.method == "GET":

        st_id = int(request.args.get('study_index'))
        st_mem = list(db.join_member.find({'study_index': st_id}))
        msg=''
        for mem in st_mem:
            u_id = mem['user_id']  # user_id
            u_name = db.user_info.find_one({'user_id': u_id})['user_name']  # user_name
            msg = msg + u_name + " "

        return jsonify({'join_member':msg});
