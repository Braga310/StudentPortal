from flask import Flask, render_template, request, url_for, redirect
from flask import flash
from pymongo import MongoClient
import random
from bson.json_util import dumps
import json
from waitress import serve
# from pymongo import MongoClient

def get_database() : 
    conntection_string = 'mongodb+srv://antisocial19845:Hello@studentportal.8c5crst.mongodb.net/?retryWrites=true&w=majority'
    client = MongoClient(conntection_string)
    return client['StudentPortal']

database = get_database()
collection_name = database['StudentData']

student_details = collection_name.find()
# print(student_details)

data = list(student_details)
data_details = dumps(data)
details = json.loads(data_details)

# print(details)
# print(type(details)) 
# print(data)

app = Flask(__name__)

@app.route('/')
def load_homepage() : 
    return render_template("html/homepage.html")

@app.route('/register.html') 
def load_registerpage() :
    return render_template("html/register.html")

@app.route('/register.html', methods=["POST"])
def register() : 
    insert = False
    if len(details) > 0 : 
        for student in details: 
            print(student)
            if request.form['registration'] == student["regNo"] : 
                # return render_template("html/login.html")
                return render_template("html/register.html" , user_exist = True)
    
    if request.form["password"] == request.form["password2"] : 
        insert = True
    
    if insert == True : 
        student = {
            "regNo" : request.form['registration'],
            "email" : request.form['email'],
            "password" : request.form['password'],
            "attendance-ai" : random.randint(70,100),
            "attendance-ds" : random.randint(70,100),
            "attendance-maths" : random.randint(70,100),
            "attendance-chemistry" : random.randint(70,100),
            "attendance-pp" : random.randint(70,100),
            "marks-ai" : random.randint(70,100),
            "marks-ds" : random.randint(70,100),
            "marks-maths" : random.randint(70,100),
            "marks-chemistry" : random.randint(70,100),
            "marks-pp" : random.randint(70,100)
        }
        collection_name.insert_one(student)
    else : 
        flash(message = "passwords doesnot match", category = 'message')
    
    # return render_template("html/login.html")
    return redirect(url_for('login'))

@app.route('/login.html')
def load_loginpage() : 
    return render_template("html/login.html")

regNo = ""
email = ""
name = ""
@app.route('/login.html', methods = ["POST"])
def login(): 
    flag = True
    found = False
    for student in details : 
        if request.form["username"] == student["regNo"] : 
            flag = False 
            if request.form["email"] == student["email"] : 
                if request.form["password"] == student["password"] : 
                    found = True
                    global regNo
                    regNo = ""
                    regNo += student["regNo"]
                    global email
                    email = ""
                    email += student["email"]
                    global name
                    name = ""
                    name += email.split(".")[0]
                    return render_template('/html/navigation.html', reg = regNo, emails = email, names = name)
                else : 
                    flag = True
                    #flash
            else : 
                flag = True
                #flash
    
    if flag == True : 
        return render_template('html/login.html' , exist = flag)
    
    if found == False : 
        return render_template('html/login.html' , user = found)

print(f"{regNo} {email} {name}")
@app.route('/navigation')
def load_navigationpage() : 
    return render_template("html/navigation.html" , reg = regNo, emails = email, names = name)

@app.route('/navigation.html')
def load_navigation() : 
    return render_template("html/navigation.html" , reg = regNo, emails = email, names = name)


@app.route('/repo.html')
def load_repository() : 
    return render_template("html/repo.html")

@app.route('/res.html')
def load_respage() : 
    return render_template("html/res.html")

@app.route('/res2.html') 
def load_res2page() : 
    return render_template("html/res2.html")

@app.route('/attendance/chemistry.html')
def load_chemistryattendance() : 
    chemistry_attendance = 0
    for stundent in details : 
        if regNo == stundent["regNo"] : 
            chemistry_attendance += stundent["attendance-chemistry"]
            break

    return render_template("html/attendance/chemistry.html", attendance = chemistry_attendance, reg = regNo, emails = email, names = name)

@app.route('/attendance/ai.html')
def load_aiattendance() : 
    ai_attendance = 0
    for stundent in details : 
        if regNo == stundent["regNo"] : 
            ai_attendance += stundent["attendance-ai"]
            break
    return render_template("html/attendance/ai.html", attendance = ai_attendance, reg = regNo, emails = email, names = name)

@app.route('/attendance/maths.html')
def load_mathsattendance() : 
    maths_attendance = 0
    for stundent in details : 
        if regNo == stundent["regNo"] : 
            maths_attendance += stundent["attendance-maths"]
            break
    return render_template("html/attendance/maths.html", attendance = maths_attendance, reg = regNo, emails = email, names = name)

@app.route('/attendance/ds.html')
def load_dsattendance() : 
    ds_attendance = 0
    for student in details : 
        if regNo == student["regNo"] : 
            ds_attendance += student["attendance-ds"]
    return render_template("html/attendance/ds.html", attendance = ds_attendance, reg = regNo, emails = email, names = name)


@app.route('/attendance/pp.html')
def load_ppattendance() : 
    pp_attendance = 0
    for student in details : 
        if regNo == student["regNo"] : 
            pp_attendance += student["attendance-pp"]
    return render_template("html/attendance/pp.html", attendance = pp_attendance, reg = regNo, emails = email, names = name)

@app.route('/results/midsem.html')
def load_midsemresult() : 
    total = 0
    for student in details : 
        if regNo == student["regNo"] : 
            m = student["marks-maths"]
            p = student["marks-pp"]
            a = student["marks-ai"]
            d = student["marks-ds"]
            c = student["marks-chemistry"]
            break
    
    total += (m + p + a + d + c)
    return render_template("html/results/midsem.html", got = total, maths = m, pp = p, ai = a, ds = d, chemistry = c, reg = regNo, emails = email, names = name)

@app.route('/results/endsems.html')
def load_endsemresult() : 
    total = 0
    for student in details : 
        if regNo == student["regNo"] : 
            m = student["marks-maths"]
            p = student["marks-pp"]
            a = student["marks-ai"]
            d = student["marks-ds"]
            c = student["marks-chemistry"]
            break
    
    total += (m + p + a + d + c)
    return render_template("html/results/endsems.html", got = total, maths = m, pp = p, ai = a, ds = d, chemistry = c, reg = regNo, emails = email, names = name)


if __name__ == '__main__' : 
    app.run(debug=True)
    # serve(app=app, host="0.0.0.0", port=50100, threads=16, url_prefix="/my-app")
