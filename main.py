from flask import *
import sqlite3 as sq

DATABASE=("./db/db.db");
app=Flask(__name__,template_folder="./template")

@app.route("/")
def main():
    getCookie = request.cookies.get('psw')
    if(getCookie != None):
        with sq.connect(DATABASE) as con:
            cur=con.cursor()
            cur.execute("SELECT * FROM tasks WHERE psw=='"+getCookie+"' ")
            result=cur.fetchall()
        data=[]
        for item in result:
            psw,task,completed =item
            data.append([psw,task,completed])
        return render_template("index.html",data=data)
    return render_template("home.html")
@app.route("/add",methods=['GET','POST'])
def add():
    if(request.method=="POST"):
        task=request.form.get("task")
        psw=request.cookies.get("psw")
        with sq.connect(DATABASE) as con:
            con.execute("INSERT INTO tasks(psw,task,completed) VALUES(?,?,?)",(psw,task,"false"))
            con.commit()
        return "<script>window.location.href='/'</script>"
    return "login plese"
@app.route("/save",methods=['GET','POST'])
def save():
    check=request.form.get("check")
    task=request.form.get("task")
    psw=request.cookies.get("psw")
    if check=="true":
        check="false"
    else:
        check="true"
    with sq.connect(DATABASE) as con:
        con.execute(" UPDATE tasks SET completed='"+check+"' WHERE task=='"+task+"' AND psw=='"+psw+"' ")
        con.commit()
    return "<script>window.location.href='/'</script>"
@app.route("/signup",methods=['GET','POST'])
def signup():
    if(request.method=="POST"):
        email=request.form.get('email')
        psw=request.form.get('psw')
        with sq.connect(DATABASE) as con:
            con.execute("INSERT INTO users(email,password) VALUES(?,?)",(email,psw))
            con.commit()
        return "<script>alert('you signup it'); window.location.href='/';</script>"
    return render_template("signup.html")
@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        email=request.form.get("email")
        psw=request.form.get("psw")
        with sq.connect(DATABASE) as con:
            cur =con.cursor()
            cur.execute("SELECT * FROM users WHERE email=='"+email+"' AND password=='"+psw+"' ")
            result=cur.fetchall()
        if result==[]:
            return "<script>alert('Try Again');window.location.href='/';</script>"
        res=make_response("<script>window.location.href='/'</script>")
        res.set_cookie("psw",psw)
        return res
    return render_template("login.html")
@app.route("/loguot")
def logout():
    resp = make_response("<script>alert('you loguot sucesfuly'); window.location.href='/';</script>")
    resp.delete_cookie('psw')
    return resp;
@app.route("/db")
def db():
    with sq.connect(DATABASE) as con:
        con.execute("CREATE TABLE tasks(psw TEXT,task TEXT,completed Text)")
        con.commit()
    return "OK" 
@app.route("/db2")
def user():
    with sq.connect(DATABASE) as con:
        con.execute("CREATE TABLE users(email TEXT,password TEXT)")
        con.commit()
    return "OK"  
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4444", debug=True)