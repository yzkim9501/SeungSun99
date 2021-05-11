import datetime
import pymongo
from flask import Blueprint, flash, render_template, request, redirect, jsonify
from auth import login_required
import db
from flask import session
import time

bp = Blueprint("board", __name__)
db = db.get_db()


@bp.route('/board')
@login_required
def board():
    return render_template('board.html')


@bp.route('/api/board_list', methods=['GET'])  # list view
@login_required
def board_list():
    board_list = list(db.board.find({}, {'_id': False}).sort('date', pymongo.DESCENDING))
    return jsonify({'board_d': board_list})


@bp.route('/board', methods=['POST'])
@login_required
def board_create():

    if request.method == "POST":
        title = request.form["post-name"]
        contents = request.form["question-content"]

        if db.board.count_documents({}) == 0:
            index = 1
        else:
            data = list(db.board.find({}, {'_id': False}).sort('date', pymongo.DESCENDING).limit(1))
            data1 = data[0]
            index = data1['index'] + 1
        dic = (
            {
                'index': index,
                'title': title,
                'contents': contents,
                'date': time.strftime('%y-%m-%d %H:%M:%S'),
                'username': session['user_name']}
        )
        db.board.insert_one(dic)
        return redirect('/board')
    return jsonify({"msg": "저장했습니다."}) and render_template("board.html")


@bp.route('/api/board_delete', methods=['POST'])
@login_required
def board_delete():
    receive_data = request.form['']
    db.board.delete_one({'': receive_data})
    return jsonify({'msg': '삭제 완료'})
