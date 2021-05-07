from flask import Flask, render_template, make_response, request, jsonify, session, redirect,g
from flask_cors import CORS, cross_origin
import requests, json, urllib
import post_message
from functools import wraps

# database setting / Hojin Lee
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbseungsun99

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'fjlkvxiwnv1v15s5v5s5s5n5b5th'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


# HTML 화면 보여주기
@app.route('/')
@cross_origin()
def home():
    if 'username' in session:
        return redirect('/study')
    else:
        return render_template('index.html')


# HTML 화면 보여주기
@app.route('/board')
@cross_origin()
@login_required
def board():
    return render_template('board.html')


# HTML 화면 보여주기
@app.route('/study')
@cross_origin()
@login_required
def study():
    return render_template('study.html')


# HTML 화면 보여주기
@app.route('/login', methods=['GET'])
@cross_origin()
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
    APP_KEY = 'Bearer xoxp-1682940574129-1936865282436-1994343867299-8015c1ba2302c4bdd8b032540f984ad5'

    # user 정보 불러올 수 있는 api url
    url = f'https://slack.com/api/users.info?user={user_id}'
    req = urllib.request.Request(url, headers={'Authorization': APP_KEY})
    res = urllib.request.urlopen(req).read()
    encoding = urllib.request.urlopen(req).info().get_content_charset('utf-8')
    JSON_object = json.loads(res.decode(encoding))

    # user name, sub name, 프로필사진 url 변수로 저장하여 study.html 파일로 패스
    first_name = JSON_object['user']['profile']['first_name']
    last_name = JSON_object['user']['profile']['last_name']
    image_192 = JSON_object['user']['profile']['image_192']
    my_res = make_response(
        render_template('study.html', first_name=first_name, last_name=last_name, image_192=image_192))

    post_message.dm(user_id, "Message here1234")  # user_id 다음의 인자 값으로 텍스트를 입력하면 슬랙 DM 으로 전송.

    session['username'] = user_id

    return my_res


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
