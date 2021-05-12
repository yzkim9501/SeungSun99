from flask import Blueprint, session, request, render_template, jsonify, redirect

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
    print(request.form)
    if request.method == "POST":
        title_receive = request.form['study-name']
        type_receive = request.form['study-type']
        level_receive = request.form['level-category']
        contents_receive = request.form['study-explain']
        time_receive = request.form['start-datetime']
        tag_along_receive = request.form['join']
        status_receive = request.form['study-status']
        num_member = request.form['study-size']


        if db.study.count_documents({}) == 0:
            index = 1
        else:
            data = list(db.study.find({}).sort('_id', pymongo.DESCENDING).limit(1))
            data1 = data[0]
            index = data1['_id'] + 1

        doc = {
            '_id': index,
            'leader_id': session['user_id'],
            'leader_name': session['user_name'],
            'study-name': title_receive,
            'study-type': type_receive,
            'level-category': level_receive,
            'study-explain': contents_receive,
            'start-datetime': time_receive,
            'join': tag_along_receive,
            'study-status': status_receive,
            'study-size': num_member,
            'date': time.strftime('%y-%m-%d %H:%M:%S')
        }


        db.study.insert_one(doc)


        return redirect(request.referrer)


@bp.route('/api/study_update', methods=["POST"])   # Update
@login_required
def study_update():
    print(request.form)
    if request.method == "POST":
        id_receive = request.form.get('study-id')

        new_title = request.form['study-name']
        new_study_type = request.form['study-type']
        new_level_category = request.form['level-category']
        new_contents = request.form['study-explain']
        new_date = request.form['start-datetime']
        new_status = request.form['study-status']
        new_size = request.form['study-size']
        new_tag_along = request.form['join']


        db.study.update_one(
            {'_id': int(id_receive)},
            {'$set': {'study-name': new_title,
                      'study-type': new_study_type,
                      'level-category': new_level_category,
                      'study-explain': new_contents,
                      'start-datetime': new_date,
                      'study-status': new_status,
                      'study-size': new_size,
                      'join': new_tag_along}}
        )


        return redirect(request.referrer)


@bp.route('/api/study_delete', methods=["GET"])     # DELETE
@login_required
def study_delete():
    id_receive = request.args.get('id')
    db.study.delete_one({'_id': int(id_receive)})

    return jsonify({'msg': '스터디 삭제 완료'})


@bp.route('/api/study_list', methods=['GET'])   # READ
@login_required
def study_list():
    study_list = list(db.study.find({}).sort('date', -1))

    return jsonify({'study_list': study_list})


@bp.route('/api/study_target', methods=['GET'])   # 해당 스터디 정보만 가져오기
@login_required
def study_target():

    id_receive = request.args.get('id')
    study_target=db.study.find_one({'_id': int(id_receive)})

    return jsonify(study_target)


@bp.route('/api/join_study', methods=['GET'])
@login_required
def join_study():

    if request.method == "GET":
        dic = (
            {
                'user_id': session['user_id'],
                'study_index': request.args.get('study_index')
            }
        )

        data = list(db.study.find_one({'_id': request.form['study_index']}))  # _id로 스터디 도큐먼트 검색.
        status = data[9]
        occ_value = status['ooc']

        num_member = data[3]
        num = num_member['study-size']

        leader_id = data[2]
        leader_id2 = leader_id['_id']

        if occ_value == 1:
            db.join_member.insert_one(dic)

            if db.join_member.count_document == num:  # 스터디정원 꽉 찼을 때.
                db.join_member.update_one({'_id': request.form['study_index']}, {'$set': {'ooc': 0}})  # ooc 0으로 업데이트

                msg = "참가인원 full, 참가자: "

                st_mem = list(db.join_member.find({'study_index': request.form['study_index']}))
                for mem in st_mem:
                    u_id = mem[0]  # user_id
                    u_name = db.user_info.find_one({'user_id': u_id})[1]  # user_name
                    msg = msg + u_name + " "
                post_message.db(leader_id2, msg)

            return jsonify({'msg': '스터디 참여 완료'})
        else:
            return jsonify({'msg': '참여 불가능'})


@bp.route('/api/exit_study')
@login_required
def exit_study():
    user_id = session['user_id']
    study_index = request.args.get('study_index')

    data = db.join_member.find({'user_id': user_id})

    for i in data:
        if i['study_index'] == study_index:
            db.join_member.delete_one({'_id': i['_id']})

    return jsonify({'msg': '삭제 완료'})


@bp.route('/api/dm_to_leader', methods=['POST'])
@login_required
def message_to_leader():
    if request.method == 'POST':
        user_name = request.form['user_name']  # 보내는 사람
        study_id = request.form['study-question-id']
        text = user_name + '님이 메세지 전송. \n' + request.form['to-leader']  # 메세지
        receiver = db.study.find_one({'_id': int(study_id)})
        receiver = receiver['leader_id']

        post_message.dm(receiver, text)

        return jsonify({'msg': '메시지 전송됨.'})
    else:
        return jsonify({'msg': '전송 실패'})


@bp.route('/api/isthismine', methods=['GET'])
@login_required
def isthismine():

    st_id = request.args.get('study_index')
    u_id = session['user_id']

    data = db.join_member.find_one({'study_index': st_id})
    if data['user_id'] == u_id:
        return jsonify({'msg': '권한승인'})
    else:
        return jsonify({'msg': '권한거부'})
