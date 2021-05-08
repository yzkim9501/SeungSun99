import datetime

from flask import Blueprint, flash, render_template, request, redirect
from auth import login_required
from db import get_db
from flask import session
import time

bp = Blueprint("board", __name__)

db = get_db()


@bp.route('/board', methods=['GET'])  # list view
@login_required
def board():
    board_list = list(db.board.find({}, {'_id': False}))
    db.board.create_index("date")
    return render_template('board.html', posts=board_list)


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
            dic = (
                {'title': title,
                 'contents': contents,
                 'date': time.strftime('%y-%m-%d %H:%M:%S'),
                 'username': session['username']}
            )

            db.board.insert_one(dic)

            return redirect('/board')

    return render_template("create.html")

