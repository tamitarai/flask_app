from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app_name = __name__ # ファイル名
app = Flask(app_name) # このインスタンスが本体になる
# ローカルで動かすPostgreSQLのパスを指定
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/flasknote"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ユーザーテーブル
class User(db.Model):
    # ユーザーテーブルの」カラムの設定
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    description = db.Column(db.String(120),index=True,unique=True)
    user_image_url = db.Column(db.String(120),index=True,unique=True)
    # インスタンス（行に相当）の出力を設定
    def __repr__(self):
        return "<User %r>"%self.username

# 新しいユーザーをDBに登録する
@app.route("/register")
def register():
    newUser = User(username="Rasmus Lerdorf",description="PHP",user_image_url="r6")
    # 行を追加
    db.session.add(newUser)
    db.session.commit()
    # ユーザー追加の結果画面を描画
    return render_template("result.html",user=newUser)


# flaskのサブコマンド（flask initdbの形で使うえる）として関数initdb_commandを実行する
@app.cli.command("initdb")
def initdb_command():
    # テーブルの初期化
    db.create_all()