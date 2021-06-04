from flask import Flask, render_template, session, redirect
import auth
import study
import board
import mypage

app = Flask(__name__)
app.secret_key = 'fjlkvxiwnv1v15s5v5s5s5n5b5th'


@app.route('/')
def home():
    if 'user_name' and 'user_id' in session:
        return redirect('/study')
    else:
        return render_template('index.html')

# 참고 사이트: https://flask.palletsprojects.com/en/1.1.x/tutorial/


app.register_blueprint(auth.bp)
app.register_blueprint(study.bp)
app.register_blueprint(board.bp)
app.register_blueprint(mypage.bp)

app.run('0.0.0.0', port=5000, debug=True)
