import pymongo

from flask import Blueprint, render_template, jsonify, request, session, redirect, make_response
import time
import db  # db.py
from auth import login_required

db = db.get_db()
bp = Blueprint('board', __name__) #Flask


##게시판 글의 CRUD기능 만들기

## HTML을 주는 부분
@bp.route('/board')  # 블루프린트 사용하기! @app.route 대신!
@login_required
def board():
    return render_template('board.html')


## (Read) 맨 처음 게시판의 목록이 보이는 것
@bp.route('/api/read_board', methods=['GET'])
@login_required
def read_board():
    total_docs = db.board.count_documents({}) ##total 갯수만.
    page_num = int(request.args.get('pageNum')) ##pageNum변수는 html에서 불러와서 그 값을 page_num에 넣음.

    if page_num == 1: ##page가 1일때
        skip_docs = 0 ##skip해야할 파일은 0개
    else:
        skip_docs = (page_num-1) * 10 ## page 2를 불러올때, 앞의 10개는 skip하고 뒤의 10개를 불러옴.

    boards = list(db.board.find({}).sort("date",-1).skip(skip_docs).limit(10))  ##에러인데 뭘 추가해야하는지 모르겠다.날짜로 sort?? 아니면 index로 sort? #datetime을 import해야함 '%Y/%m/%d %H:%M:%S'를 먼저 정의하나?
    return jsonify({'total': total_docs, 'all_boards': boards})


## (Create & Update) API 역할을 하는 부분  (이 부분 조언 구하기)
## title 미작성시 글이 작성되는 것을 막아야함.
@bp.route('/api/create_board', methods=['POST'])
@login_required
def create_board():
    if request.method == "POST":
        title = request.form["post-name"]
        question_content = request.form["post-content"]

        # (Create를 할때!)게시물 인덱싱 조건문 추가
        if db.board.count_documents({}) == 0:
            index = 1
        else:  # document 가 있으면
            data = list(db.board.find({}).sort('_id', pymongo.DESCENDING).limit(1))
            data1 = data[0]
            index = data1['_id'] + 1


        doc = ({
                   '_id': index,
                   'post-name': title,
                   'post-content': question_content,
                   'date': time.strftime('%y-%m-%d %H:%M:%S'),
                   'user_id': session['user_id'],
                   'user_name': session['user_name'],
        })


        db.board.insert_one(doc)

        return redirect(request.referrer)


@bp.route('/api/update_board', methods=['POST'])
@login_required
def update_board():
    if request.method == "POST":
        id_receive = request.form.get('board-id')
        data = db.board.find_one({'_id': int(id_receive)})

        if session.get('user_id') == data['user_id']:
            new_title = request.form['post-name'],
            new_content = request.form['post-content']

            db.board.update_one({'_id': int(id_receive)},
                                {'$set': {'post-name': new_title,
                                          'post-content': new_content}})
            return redirect(request.referrer)
        else:
            return jsonify({'msg': '권한이 없습니다.'})


@bp.route('/api/delete_board', methods=['GET'])
@login_required
def delete_board():
    delete1 = request.args.get('index')
    data = db.board.find_one({'_id': int(delete1)})

    if session.get('user_id') == data['user_id']:
       db.board.delete_one({'_id': int(delete1)})

       return jsonify({'msg': '게시물이 삭제되었습니다.'})
    else:
       return jsonify({'msg': '권한이 없습니다..'})


@bp.route('/api/board_target', methods=['GET'])
@login_required
def board_target():
    target = request.args.get('index')
    board_target = db.board.find_one({'_id': int(target)}) ##int와 같이 알고 있는 부분도 구현할 수 있도록 해보자
    return jsonify(board_target)

