from flask import Flask, render_template, make_response, request, jsonify
from flask_cors import CORS, cross_origin
import requests, json, urllib

# database setting / Hojin Lee
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbseungsun99

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# HTML 화면 보여주기
@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')


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
    return my_res


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
