# %%[]
from datetime import datetime
from flask import Flask,redirect,url_for,render_template,request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,logout_user,login_user,login_required,current_user
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from rauth import OAuth1Service
from requests_oauthlib import OAuth1Session

API_KEY="vvdDIm6jHCbsAIXtcFF5gL9GE"
API_SECRET_KEY="JELo09f71nB3pDaKTRex5HN4flvl7g3znNqB7dgnCHOTZGZ4Xq"
ACCESS_TOKEN="508749902-DxmqVx3WvfB44PjhQbiMhjgdvZFWhSAhRAaT6I8S"
ACESS_TOKEN_SECRET="BpJK1UJyOu59TSJlD483Ulrs6OPljDHxQknsvzEoigkYj"

app_name = __name__ # ファイル名
app = Flask(app_name) # このインスタンスが本体になる
# ログイン用のインスタンスを初期化
login_manager=LoginManager()
login_manager.init_app(app)

# ローカルで動かすPostgreSQLのパスを指定
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/testdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wj9jr2jg@249j0J4h20JaV91A03f4j2'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
# Oauthの認証をするクライアント
service = OAuth1Service(
    name="twitter",
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    request_token_url='https://api.twitter.com/oauth/request_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    access_token_url='https://api.twitter.com/oauth/access_token',
    base_url='https://api.twitter.com/1.1/'
)
# service = OAuth1Session(API_KEY,API_SECRET_KEY)
# service.fetch_request_token('https://api.twitter.com/oauth/request_token')
# authUrl = twitter.authorization_url('https://api.twitter.com/oauth/authorize')


# ユーザーテーブル
class User(UserMixin,db.Model):
    # ユーザーテーブルの」カラムの設定
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    description = db.Column(db.String(120),index=True,unique=True)
    user_image_url = db.Column(db.String(120),index=True,unique=True)
    date_published = db.Column(db.DateTime,server_default=datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"))
    twitter_id = db.Column(db.String(64),unique=True)
    # インスタンス（行に相当）の出力を設定。
    # __repr__はインスタンス自体をprintした場合などの出力形式を設定するもの
    def __repr__(self):
        return '<User %r>'%self.username

# 質問テーブル
class Question(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(256))
    profile_image_url = db.Column(db.String(1024))
    date_published = db.Column(db.DateTime,default=datetime.utcnow())
    # 外部キー
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    answerer_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    answer_image_url = db.Column(db.String(1024))
    answer_body = db.Column(db.String(256))
    def __repr__(serlf):
        return '<Question %r>'%self.body

@app.cli.command('initdb')
def initdb_command():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

# ログアウト処理
@app.route("/logout")
@login_required
def logout():
    logout_user()
    # トップページにリダイレクト
    return redirect(url_for("index"))

@app.route("/user/<id>")
def user(id):
    '''URLに含まれるIDを受け取って、そのユーザー情報と質問を返す'''
    user = User.query.get(int(id))
    # もしユーザーがいたら
    if user:
        # ユーザーIDと一致するanswerIDを持ってる質問を全部取得する
        questions = db.session.query(Question).filter(Question.answerer_id==id).all()
        # 取得したユーザー情報と質問をわたす
        return render_template("user.html",user=user,questions=questions)
    else:
        return render_template("error.html")

@app.route("/question",methods=["POST"])
@login_required
def question():
    '''新たに質問がきたら追加する'''
    if request.form["body"]:
        # 新しい質問を追加
        newQuestion = Question(
            body=request.form["body"],
            profile_image_url=current_user.user_image_url,
            user_id=current_user.id,
            answerre_image_url=request.form["answer_image_url"],
            answerer_id=request.form["answerrer_id"]
        )
        db.session.add(newQuestion)
        db.session.commit()
        return render_template("index.html")
    else:
        return render_template("error.html")

@app.route("/answer_to/<id>",methods=["GET"])
@login_required
def answers(id):
    '''指定されたIDの質問を取得して、それが現在ユーザーのIDと一致してたら返す'''
    question = Question.query.get(int(id))
    if int(question.answerer_id) == int(current_user.id):
        return render_template("answer.html",question=question)

@app.route("/answer",methods=["POST"])
@login_required
def answer():
    # 要求されたIDと一致する質問があればとってくる
    question = db.session.query(Question).filter(Question.id==int(request.form["id"])).first()
    # answer_idとユーザーIDが一致していて、かつanswer_bodyが入力されていたら,
    # とってきた質問のanswer_bodyに投稿されたanswer_bodyを入力する
    if int(question.answer_id)==int(current_user.id) and request.form["answer_body"]:
        question.answer_body = request.form["answer_body"]
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("error.html")



@app.route("/oauth/twitter")
def oauth_authorize():
    # current_userってなんだっけ？
    if not current_user.is_anonymous:
        # アノニマスならホームディレクトリへリダイレクト
        return redirect(url_for("index"))
    else:
        # リクエストトークンをTwitter APIから取得
        request_token=service.get_request_token(
                params={
                    "oauth_callback ":
                        url_for(
                        "oauth_callback",
                        provider="twitter",
                        _external=True)
                }   
            )
        # セッションにトークンを渡す
        session["request_token"] =request_token
        # Twitter連携認証の画面にリダイレクト
        redirect_result = service.get_authorize_url(request_token[0])
        return redirect(redirect_result)

# ログイン処理
# Twitterのログインページにリダイレクトれたユーザーがボタンを押すとここにリダイレクトされる
@app.route("/oauth/twitter/callback")
def oauth_callback():
    request_token=session.pop("request_token")
    # セッションを取得
    oauth_session=service.get_auth_session(
        request_token=request_token[0],
        request_token_secret=request_token[1],
        data={
            "oauth_verifier":request.args["oauth_verifier"]
        }
    )
    # セッションからアカウントのプロフィールを取得
    profile = oauth_session.get("account/verify_credentials.json").json()
    twitter_id = str(profile.get("id"))
    username=str(profile.get("name"))
    description=str(profile.get('description'))
    profile_image_url = str(profile.get('profile_image_url'))
    # Twitter Oauthの情報から、DBのユーザーを取得
    # try:
    user = db.session.query(User).filter(User.twitter_id==twitter_id).first()
    # もし
    if user:
        user.twitter_id  = twitter_id
        user.username = username
    else:
        user = User(
            twitter_id=twitter_id,
            username=username,
            description=description,
            user_image_url=profile_image_url)
        # dbのセッションに追加して
        db.session.add(user)
        # 最終的にadd
    db.session.commit()
    # このユーザー情報を元にセッションを生成
    login_user(user,True)
    # ホームディレトリにリダイレクト
    return redirect(url_for("index"))

# セッションを保持
# セッション情報とユーザー情報を照合して相違がなければセッションを維持
@login_manager.user_loader
def load_user(id): # この引数なんだっけ？
    return User.query.get(int(id))