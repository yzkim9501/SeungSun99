from flask import Blueprint, session, request, render_template, jsonify

import post_message
from auth import login_required
import db
import pymongo
import time
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
            'leader_id': session['user_id'],
            'leader_name': session['user_name'],
            'title': title_receive,
            'study-type': type_receive,
            'level-category': level_receive,
            'contents': contents_receive,
            'date': time.strftime('%y-%m-%d %H:%M:%S'),
        }

        db.study.insert_one(doc)


        return jsonify({'msg': '스터디 생성 완료!'})


@bp.route('/api/study_update', methods=["POST"])   # Update
@login_required
def study_update():
    if request.method == "POST":
        title_receive = request.form['title']
        target_study = db.study.find_one({'title': title_receive})

        new_title = target_study['title']
        new_study_type = target_study['study-type']
        new_level_category = target_study['level-category']
        new_contents = target_study['contents']
        new_date = target_study['date']


        db.study.update_one(
            {'title': title_receive},
            {'$set': {'title': new_title,
                      'study-type': new_study_type,
                      'level-category': new_level_category,
                      'contents': new_contents,
                      'date': new_date}}
        )


        return jsonify({'msg': '스터디 수정 완료!'})


@bp.route('/api/study_delete', methods=["GET"])     # DELETE
@login_required
def study_delete():
    title_receive = request.form.get['title']
    db.study.delete_one({'title': title_receive})

    return jsonify({'msg': '스터디 삭제 완료'})


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


@bp.route('/api/dm_to_leader', methods=['POST'])
@login_required
def message_to_leader():
    if request.method == 'POST':
        user_name = request.form['user_name']  # 보내는 사람
        study_id = request.form['study_id']
        text = user_name + '님이 메세지 전송. \n' + request.form['to-leader']  # 메세지
        receiver = db.study.find_one({'_id': study_id})
        receiver = receiver['leader_id']

        post_message.dm(receiver, text)

        return jsonify({'msg': '메시지 전송됨.'})
    else:
        return jsonify({'msg': '전송 실패'})


