from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from datetime import datetime

app_name = __name__ # ファイル名
app = Flask(app_name) # このインスタンスが本体になる
# ローカルで動かすPostgreSQLのパスを指定
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost/testdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ユーザーテーブル
class User(db.Model):
    # ユーザーテーブルの」カラムの設定
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    description = db.Column(db.String(120),index=True,unique=True)
    user_image_url = db.Column(db.String(120),index=True,unique=True)
    # インスタンス（行に相当）の出力を設定。
    # __repr__はインスタンスをprintした場合などの出力形式を設定するもの
    def __repr__(self):
        return "<User %r"%self.username

# ユーザーテーブルの全レコードを取得して、index.htmlに渡す
@app.route("/")
def index():
    # ユーザーテーブルの全レコードを取得
    users = User.query.all()
    return render_template("index.html",users=users)

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