from flask import Blueprint, session, request, render_template, jsonify

import post_message
from auth import login_required
import db
import pymongo
bp = Blueprint("study", __name__)

db = db.get_db()


@bp.route('/study')
@login_required
def study():
    return render_template('study.html')


@bp.route('/api/study', methods=["POST"])  # 스터디 생성 데이터 저장
@login_required
def study_create():
    if request.method == "POST":
        title_receive = request.form['title']
        type_receive = request.form['study-type']
        level_receive = request.form['level-category']
        contents_receive = request.form['contents']

        doc = {
            'title': title_receive,
            'study-type': type_receive,
            'level-category': level_receive,
            'contents': contents_receive,
            'date': time.strftime('%y-%m-%d %H:%M:%S'),
        }

        db.study.insert_one(doc)

        return jsonify({'msg': '스터디 생성 완료!'})


@bp.route('/api/study', methods=["POST"])   # Update
@login_required
def study_update():
    if request.method == "POST":
        title_receive = request.form['title']
        target_study = db.study.find_one({'title':title_receive})

        new_title = target_study['title']
        new_study-type = target_study['study-type']
        new_level-category = target_study['level-category']
        new_contents = target_study['contents']
        new_date = target_study['date']


        db.study.update_one(
            {'title': title_receive},
            {'$set': {'title': new_title,
                      'study-type': new_study-type,
                      'level-category': new_level-category,
                      'contents': new_contents,
                      'date': new_date}}
        )


        return jsonify({'msg': '스터디 수정 완료!'})



@bp.route('/api/study_list', methods=['GET'])   # READ
@login_required
def study_list():
    study_list = list(db.study.find({}, {'_id': False}).sort('date', -1))

    return jsonify({'study_list': study_list})


@bp.route('/api/join_study')
@login_required
def join_study():
    dic = (
        {
            'user_id': session['user_id'],
            'study_index': request.form['study_index']
        }
    )
    db.join_member.insert_one(dic)

    return jsonify({'msg': '스터디 참여 완료'})


@bp.route('/api/exit_study')
@login_required
def exit_study():
    user_id = session['user_id']
    db.join_member.delete_one({'user_id': user_id})

    return jsonify({'msg': '삭제 완료'})


@bp.route('/study', methods=['POST'])
@login_required
def message_to_leader():
    if request.method == 'POST':
        id = session['user_name']
        text = id + '님이 메세지 전송. \n' + request.form['to-leader']

        post_message.dm(session['user_id'], text)

        return jsonify({'msg': '메시지 전송됨.'})
    else:
        return jsonify({'msg': '전송 실패'})


