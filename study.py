import datetime

from flask import Blueprint, flash, render_template, request, redirect
from auth import login_required
from db import get_db
from flask import session
import time

bp = Blueprint("study", __name__)

db = get_db()


@bp.route('/study')
@login_required
def study():
    return render_template('study.html')

@bp.route('/study', methods=["GET", "POST"])
@login_required
def study_create():
    if request.method == "POST":

        title = request.form.get("title")
        contents = request.form.get("contents")
        type = request.form.get("type")
        level = request.form.get("level")

        to_db = {
            "title": title,
            "contents": contents,
            "type": type,
            "level": level,
            "view": 0,
            "date": time.strftime('%y-%m-%d %H:%M:%S')
        }
        db.study.insert_one(to_db)

        return render_template("study.html")
    else:
        return render_template("study.html")

