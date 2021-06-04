from functools import wraps
from flask import session, redirect, request, render_template, make_response, Blueprint, jsonify

import requests
import json
import urllib

import post_message

import db

db = db.get_db()

bp = Blueprint("auth", __name__)


def login_required(f):
    @wraps(f)
    def wrap(**kwargs):
        if 'user_name' and 'user_id' in session:
            return f(**kwargs)
        else:
            return redirect('/')

    return wrap


@bp.route('/login', methods=['GET'])
def login():
    # 코드변수 저장
    receive_code = request.args.get('code')

    # 유저 아이디 가져올 수 있는 api url
    get_user_id_url = f'https://slack.com/api/oauth.v2.access?client_id=1682940574129.1987342115286&client_secret=2600ed20347e595da2812d5935658caa&code={receive_code}'
    res = requests.get(get_user_id_url)
    res_json = json.loads(res.text)

    if not res_json['ok']:
        return render_template('study.html')

    # user id 저장
    user_id = res_json['authed_user']['id']

    # slack app key 저장
    APP_KEY = 'Bearer xoxp-1682940574129-1936865282436-2102798542897-9c5fae67f4b1509548b28201dd1a948c'

    # user 정보 불러올 수 있는 api url
    url = f'https://slack.com/api/users.info?user={user_id}'
    req = urllib.request.Request(url, headers={'Authorization': APP_KEY})
    res = urllib.request.urlopen(req).read()
    encoding = urllib.request.urlopen(req).info().get_content_charset('utf-8')
    JSON_object = json.loads(res.decode(encoding))
    print(JSON_object)
    # user name, sub name, 프로필사진 url 변수로 저장하여 study.html 파일로 패스
    first_name = JSON_object['user']['profile']['first_name']
    last_name = JSON_object['user']['profile']['last_name']
    image_192 = JSON_object['user']['profile']['image_192']

    # post_message.dm(user_id, "Message here1234")  # user_id 다음의 인자 값으로 텍스트를 입력하면 슬랙 DM 으로 전송.

    session['user_name'] = first_name
    session['sub_name'] = last_name
    session['img_url'] = image_192
    session['user_id'] = user_id

    if db.user_info.find_one({'user_id': user_id}):
        pass
    else:
        db.user_info.insert_one({
            'user_id': user_id,
            'user_name': first_name
        })

    return render_template('study.html')


@bp.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    session.pop('sub_name', None)
    session.pop('img_url', None)
    return jsonify({'msg': '로그아웃 완료'}) and redirect('/')
