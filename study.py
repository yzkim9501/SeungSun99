from flask import Blueprint, session, request, render_template, jsonify
from auth import login_required
import db
import pymongo
bp = Blueprint("study", __name__)

db = db.get_db()


@bp.route('/study')
@login_required
def study():
    return render_template('study.html')


@bp.route('/api/study_list', methods=['GET'])
@login_required
def study_list():
    study_list = list(db.study.find({}))

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

