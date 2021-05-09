from flask import Blueprint, render_template
from auth import login_required
import db
import pymongo  # 정렬 기능이 여깄음 ㅇㅅㅇ;;
bp = Blueprint("study", __name__)

db = db.get_db()


@bp.route('/study')
@login_required
def study():
    study_list = list(db.study.find({}).sort('date', pymongo.ASCENDING))

    return render_template('study.html', posts=study_list)


# @bp.route('/board', methods=['GET'])  # list view
# @login_required
# def board():
#     board_list = list(db.board.find({}, {'_id': False}).sort('date', pymongo.DESCENDING))
#     index = board_list[0]
#     print(index['index'])
#     return render_template('board.html', posts=board_list)