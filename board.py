import pymongo

from flask import Flask, Blueprint, render_template, jsonify, request, session
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
    boards = list(db.board.find({}, {'_id': False}).sort('date',pymongo.descending))  ##에러인데 뭘 추가해야하는지 모르겠다.날짜로 sort?? 아니면 index로 sort? #datetime을 import해야함 '%Y/%m/%d %H:%M:%S'를 먼저 정의하나?
    return jsonify({'all_boards': boards})


## (Create & Update) API 역할을 하는 부분  (이 부분 조언 구하기)
@bp.route('/api/create_board', methods=['POST'])
@login_required
def create_board():
    if request.method == "POST":
        post_title = request.form["post_title"]
        question_contents = request.form["question-content"]  ## 구글링으로 일단 넣었다 ,,,,

        doc = ({
                   'index': index,  # 게시판 인덱스는 숫자로
                   'title': title,
                   'contents': contents,
                   'date': time.strftime('%y-%m-%d %H:%M:%S'), ##해결!
                   'user_id': session['user_id'],
                   'user_name': session['user_name'],  ## How? 유저아이디인지 유저이름인지 확인필요 따로따로 저장하고 표시는 이름으로
        })
        db.board.update_one({}, {'$set': {'index': +1}})
        ##업데이트시, 1)정보를 불러와야함 2)새로 입력한 값으로 바꿈.
        ## 오후 할일 1순위 다시 찾아보자
        db.board.insert_one(doc)

        return jsonify({'msg': '게시판에 글이 작성되었습니다.'})


    ## (Delete) index를 받아서 get 방식으로 게시물 글 지우기!

@bp.route('/api/delete_board', methods=['GET'])
@login_required
def delete_board():
    delete1: request.args.get('index')
    db.board.delete_one({'index': 'delete1'})
    return jsonify({'msg': '삭제되었습니다'})
    ##삭제시 비밀번호 필요한가?
    ##remove???
    ##게시글 수정도 하나..?