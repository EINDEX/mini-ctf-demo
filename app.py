from flask import Flask, redirect, request, Blueprint, render_template, send_file, make_response
import yaml
import pathlib
import os
import jwt
import sqlite3
import urllib



with open('config.yaml') as f:
    config = yaml.load(f, yaml.Loader)

app = Flask(__name__)

app_secret = config.get('seecret', "")

def check(username, password):
    conn = sqlite3.connect('data.db')
    statement = 'select username, password from user where username="'+ username + '" and password ="'+password+'"'
    res = conn.execute(statement).fetchall()
    is_success = len(res) > 0
    conn.close()
    return is_success




@app.route("/")
def hello_world():
    return redirect("/login", code=301)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            if (username == config['admin']['username'] and password == config['admin']['password']) or check(username, password):
                resp = redirect("/me")
                encoded_jwt = jwt.encode({"username": username}, app_secret, algorithm="HS256")
                resp.set_cookie("auth", f"{encoded_jwt}")
                return resp
            else:
                return redirect("/login?message=username%20and%20password%20are%20not%20currect%3F%3Cbr%3E%20not%20have%20account%20you%20can%20go%20%3Ca%20href%3D%22%2Freg%22%3Eregister%3C%2Fa%3E%20a%20account.")
        except Exception as e:
            return redirect('/login?message='+urllib.parse.quote(str(e)))

@app.route("/reg", methods=["GET","POST"])
def reg():
    if request.method == "GET":
        return render_template("reg.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            conn = sqlite3.connect('data.db')
            statement = f'insert into user (username, password) values ("{username}", "{password}")'
            res = conn.execute(statement)
            conn.commit()
            conn.close()
            if res.rowcount >= 1:
                return redirect("/login?message=register success.")
            else:
                return redirect("/reg?message=some thing not right.")
        except Exception as e:
            return redirect("/reg?message="+urllib.parse.quote(str(e)))
            
        


@app.route("/logout", methods=["GET"])
def logout():
    resp = redirect("/login")
    resp.delete_cookie("auth")
    return resp

@app.route("/me", methods=["GET"])
def me():
    auth_cookie = request.cookies.get("auth","")
    if not auth_cookie:
        return redirect("/login?message=how did you know this page? but not success :)")
    try:
        jwt_token = auth_cookie
        data = jwt.decode(jwt_token, app_secret, algorithms=["NONE", "None", "HS256", None])
        username = data.get("username", "you")
        result = f"Welcome {username}!"
        if username == "admin":
            result += "<br>Congratulations!! the token is '19c49cfb32d4a43c4e19e32cb0d2b4c1'!"
        result += '<br><a href="/logout">Logout</a>'
        return result
    except Exception as e:
        raise e
        return str(e)

@app.route('/files/', defaults={'req_path': '.'})
@app.route('/files/<path:req_path>')
def file_path(req_path):
    if pathlib.Path(req_path).is_dir():
        return "<br>".join(os.listdir(req_path))
    with open(req_path, 'r') as f:
        return f.read().replace('\n', '<br>')


"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.B_ej7DU2M0tah3XKHi8vhWBGqGyRj5I3BctaHubHDcY"
'{"typ":"JWT","alg":"NONE"}'
"eyJ0eXAiOiJKV1QiLCJhbGciOiJOT05FIn0.eyJ1c2VybmFtZSI6ImFkbWluIn0."