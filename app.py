from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import psycopg2 
import psycopg2.extras

app_name = __name__ # ファイル名
app = Flask(app_name) # このインスタンスが本体になる

conn = psycopg2.connect(" user=postgres dbname=testdb password=postgres")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# bootstrapで作ったhtmlを表示。「アンサ」をクリックするとrootに飛ぶ。
@app.route("/",methods=["GET"])
def bootstrap():
  return render_template("index.html")

@app.route("/login",methods=["GET"])
def render_form():
  return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
  if request.form["email"] and request.form['username']:
    return render_form("check.html",username=request.form['username'],email=request.form["email"])
  else:
    return render_form("error.html")


# uploadしてくれ画面を表示
@app.route("/upload",methods=["GET"])
def render_upload_from():
  return render_template("upload.html")

# uploadされた後の画面を表示
@app.route("/upload",methods=["POST"])
def upload_file():
  # upload.htmlで定めたnameがキーになる
  if request.form["name"] and request.files["image"]:
    f = request.files["image"]
    # 適当な文字列に変換
    filepath = 'static/' + secure_filename(f.filename)
    # とりあえずアップロードされたものはローカル保存
    f.save(filepath)
    return render_template("result.html",name=request.form["name"],image_url=filepath)

# 継承の例
@app.route("/inheritance")
def index_inheritance():
  return render_template("index_inheritance.html",title="Hoge",message="Fuga")

# タグがそのまま見える
@app.route("/unescape")
def unescape():
  return render_template("unescape.html",unescaped="<script>alert('hoge')</script>")

# html側のif文によって、リロードするたびに表示が変わる
import random
@app.route("/random")
def random_render():
  return render_template("random.html",random=random.random())

# 以下のようにアクセスすると、hogehogを表示する
# http://localhost:5000/search?q=hogehoge
@app.route("/search")
def search():
    q = request.args.get("q","")
    return q

@app.route('/user/<int:id>') # int型だけ受け付ける
def user_id(id):
    return str(id)

# <title>は、<>の中に入れた文字列をルーティングの関数の中で使えるよ、ということ
@app.route("/title/<title>",methods=["GET"])
# <title>に指定した値は、関数titleの引数として渡される
def title(title):
    # htmlのテンプレートエンジンにtitleという変数として渡される
    # すると、index.htmlの{title}となっている部分に変数が設定されてレンダリングされる
    return render_template("index.html", title=title)

# # これは、user/mitaraiとかでアクセスすると画面上にmitaraiとか出てくる
# @app.route("/user/<username>")
# def user(username):
#     return username

# @app.route("/",methods=["GET"])
# def hello_world():
#     return """
#         <!DOCTYPE html>
#         <html>
#           <head>
#             <meta charset="utf-8"/>
#             <link rel="stylesheet" href="/static/style.css"/>
#           </head>
#           <body>
#             <h1>Hello World</h1>
#           </body>
#         </html>
#     """

@app.route("/hoge",methods=["GET"])
def hoge():
    return "hoge"