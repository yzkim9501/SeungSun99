import datetime

import pymongo
from flask import Blueprint, flash, render_template, request, redirect
from auth import login_required
import db
from flask import session
import time

bp = Blueprint("board", __name__)

db = db.get_db()


@bp.route('/board', methods=['GET'])  # list view
@login_required
def board():
    board_list = list(db.board.find({}, {'_id': False}).sort('date', pymongo.DESCENDING))
    index = board_list[0]
    print(index['index'])
    return render_template('board.html', posts=board_list)


@bp.route('/board/view', methods=['GET'])
@login_required
def board_view():
    data = list(db.board.find({}))
    print(data)

    return render_template('view.html')


@bp.route('/board/create', methods=("GET", "POST"))
@login_required
def create():
    print(session['username'])
    if request.method == "POST":
        title = request.form["title"]
        contents = request.form["contents"]

        if not title:
            error = "Title is required"
        else:
            error = None

        if error is not None:
            flash(error)
        else:
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
                    'username': session['username']}
            )

            db.board.insert_one(dic)

            return redirect('/board')

    return render_template("create.html")


