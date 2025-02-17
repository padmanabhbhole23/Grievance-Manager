from flask import Flask,render_template,request,make_response
import mysql.connector as mysql
from datetime import datetime
current_date = datetime.now().strftime("%d %b,%Y")

connection=mysql.connect(host="localhost",user="root",password="123456",database="GrievanceSys")
cursorPy=connection.cursor()

app=Flask(__name__)
@app.route("/")
def hello():
    return render_template('index.html',info=[],length=0,totalStud=0,totalStaff=0,date=current_date)

@app.route("/selectData",methods=["POST"])
def selectDataFromDB():
    if request.method=="POST":
        dept=request.form.get("dept")
        role=request.form.get("role")

        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s",(role,dept,))
        data=cursorPy.fetchall()
        print(data)

        # Set Data in notification panel
        totalGrev=len(data)

        # set data student total grivence
        C1role="Student"
        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s", (C1role,dept,))
        data2 = cursorPy.fetchall()
        totalStudGrv=len(data2)

        # set data stff total grivence
        C2role = "Staff"
        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s",(C2role, dept,))
        data3 = cursorPy.fetchall()
        totalStaffGrev=len(data3)

        if not data:
            resp=make_response(render_template('index.html',info=[],length=0,totalStud=0,totalStaff=0,date=current_date))
            resp.set_cookie("dept", dept if dept else "")
            resp.set_cookie("role", role if role else "")

            return resp
        else:
            resp = make_response(render_template('index.html', info=data, length=totalStudGrv, totalStud=totalStudGrv, totalStaff=totalStaffGrev, date=current_date))
            resp.set_cookie("dept", dept if dept else "")
            resp.set_cookie("role", role if role else "")
            return resp


@app.route("/reject",methods=["POST"])
def deleteGrev():
    if request.method=="POST":
        dept=request.cookies.get("dept")
        role=request.cookies.get("role")
        id=request.form.get("gid")

        cursorPy.execute("delete from GrievanceSys where GrievanceId=%s and Role=%s and Dept=%s",(id,role,dept,))
        connection.commit()
        # send fresh data agin ------------------------------

        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s", (role, dept,))
        data = cursorPy.fetchall()
        print(data)

        # Set Data in notification panel
        totalGrev = len(data)

        # set data student total grivence
        C1role = "Student"
        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s",(C1role, dept,))
        data2 = cursorPy.fetchall()
        totalStudGrv = len(data2)

        # set data stff total grivence
        C2role = "Staff"
        cursorPy.execute("select GrievanceId,Grievance,Date from GrievanceSys where Role=%s and Dept=%s",(C2role, dept,))
        data3 = cursorPy.fetchall()
        totalStaffGrev = len(data3)

        if not data:
            return render_template('index.html', info=[], length=0, totalStud=0, totalStaff=0, date=current_date)
        else:
            return render_template('index.html', info=data, length=totalStudGrv, totalStud=totalStudGrv, totalStaff=totalStaffGrev, date=current_date)
    else:
        print("This is not important")


app.run()