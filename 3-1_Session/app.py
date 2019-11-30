# %%[]
from datetime import datetime
from flask import Flask,redirect,url_for,render_template,request,make_response,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,logout_user,login_user,current_user
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from rauth import OAuth1Service
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
migrate = Migrete(app,db)

@app.route("/")
def index():
    if "logged_in" in session and session["logged_in"]==True:
        return "You are logged in"
    # もしsessionに"logged_in"が無ければ、sessin["logged_in"]をTrueにしておく
    # これで、次からは"You are logged in"が表示される
    else:
        session["logged_in"] = True
        return "You are not logged in"
    try:
        # cookieにおける"count"の数を受け取る
        count = request.cookies.get("count")
        # countがrequestオブジェクト内に既にあればあれば、countに+1
        if count != None:
            count = int(count)+1
        # countがrequest内になければ、countを0に初期化
        else:
            count=0
        # index.htmlの結果を受け取る
        resp=make_response(render_template("index.html",count=count))
        # cookieに、countを追加する
        resp.set_cookie("count",str(count))
        return resp
    except Exception as e:
        return render_template("error.html"),500


# ログアウト処理
@app.route("/logout")
@login_required
def logout():
    logout_user()
    # トップページにリダイレクト
    return redirect(url_for("index"))


# セッションを保持
# セッション情報とユーザー情報を照合して相違がなければセッションを維持
@login_manager.user_loader
def load_user(id): # この引数なんだっけ？
    return User.query.get(int(id))

# lgoin_userインスタンスに登録されたユーザーのみが利用できる
@login_required
def settings():
    pass


@app.route("/form")
def form():
    return render_template("form.html")

# 新たなユーザーのレコードを追加する
@app.route("/register", methods=["POST"])
def register():
    # from.htmlで入力されたなかにusernameとdescriptionとimageがあったら
    # imageを保存する
    if request.form["username"] and request.form["description"] and request.files["image"]:
        f = request.files["image"]
        filepath = "static/"+secure_filename(f.filename)
        f.save(filepath)
        
        newUser = User(username=request.form["username"],
            description=request.form["description"],
            user_image_url=filepath
            )
        # DBを更新する
        # まずセッションを更新して
        db.session.add(newUser)
        # それをコミットして更新 
        db.session.commit() 
        return render_template("result.html",username=request.form["username"],description=request.form["description"],user_image_url=filepath)
    # 入力が足りない場合はエラー
    else:
        return render_template("error.html")

# flask initdbというコマンドで、DBを初期化してORMで設定したテーブルを作れる
@app.cli.command("initdb")
def initdb_command():
    db.create_all()