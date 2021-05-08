from flask import Flask, render_template, session, redirect
import auth
import study
import board

app = Flask(__name__)
app.secret_key = 'fjlkvxiwnv1v15s5v5s5s5n5b5th'


@app.route('/')
def home():
    if 'username' in session:
        return redirect('/study')
    else:
        return render_template('index.html')


app.register_blueprint(auth.bp)
app.register_blueprint(study.bp)
app.register_blueprint(board.bp)

app.run('127.0.0.1', port=5000, debug=True)
