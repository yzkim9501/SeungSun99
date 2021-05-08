from flask import Blueprint, render_template
from auth import login_required

bp = Blueprint("study", __name__)


@bp.route('/study')
@login_required
def study():
    return render_template('study.html')