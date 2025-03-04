from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector as mysql
from datetime import datetime

#  Flask app Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

#  MySQL database Connection
connection = mysql.connect(host="localhost", user="root", password="123456", database="GrievanceSys")
cursorPy = connection.cursor()
current_date = datetime.now().strftime("%d %b, %Y")

#Below code contains all the routingz
# -------------------------- DASHBOARD --------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template('userDash.html')

# -------------------------- LOGIN --------------------------
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check user credentials
        cursorPy.execute("SELECT UID, UName, UDept, URole FROM Users WHERE UEmail=%s AND UPass=%s", (email, password))
        user = cursorPy.fetchone()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["dept"] = user[2]
            session["role"] = user[3]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid email or password!")

    return render_template("login.html")

# -------------------------- ADD GRIEVANCE --------------------------
@app.route("/AdGrev", methods=["GET", "POST"])
def add_grievance():
    if request.method == "POST":
        grievance_text = request.form.get("grievance")

        # Insert grievance into database
        cursorPy.execute(
            "INSERT INTO GrievanceSys (Grievance, Role, Dept, Date, Status) VALUES (%s, %s, %s, %s, %s)",
            (grievance_text, session['role'], session['dept'], current_date, "Raised")
        )
        connection.commit()

        # Fetch the last inserted grievance ID
        cursorPy.execute("SELECT LAST_INSERT_ID()")
        grievance_id = cursorPy.fetchone()[0]
        session["grievance_id"] = grievance_id


        return f'''
               <script>
                   alert("Grievance ID {grievance_id} submitted successfully!");
                   window.location.href = "/dashboard";
               </script>
           '''
    return render_template('AdGrev.html')

# -------------------------- TRACK GRIEVANCE --------------------------
@app.route("/TrackGrie", methods=["GET", "POST"])
def track_grievance():
    grievance_id = session.get("grievance_id")  # Fetch last submitted grievance
    grievance_status = "Not Found"
    progress = 0
    reported_datetime = "Unknown"

    if request.method == "POST":
        grievance_id = request.form.get("grievance_id")  # User input

    if grievance_id:
        cursorPy.execute("SELECT Status, Date FROM GrievanceSys WHERE GrievanceId=%s", (grievance_id,))
        result = cursorPy.fetchone()

        if result:
            grievance_status, reported_datetime = result

            # Map status to progress
            progress_mapping = {
                "Raised": 0,
                "Assigned": 30,
                "Processing": 70,
                "Resolved": 100
            }
            progress = progress_mapping.get(grievance_status, 0)
        else:
            grievance_status = "Grievance ID not found."

    return render_template('TrackGrie.html', grievance_status=grievance_status, grievance_id=grievance_id,
                           progress=progress, reported_datetime=reported_datetime)


# -------------------------- UPDATE ACCOUNT --------------------------
@app.route("/Update")
def update_account():
    return render_template('Update.html')

# -------------------------- LOGOUT --------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------- REISSUE --------------------------
@app.route("/reissue", methods=["GET", "POST"])
def reissue():
    return render_template('AdGrev.html')

# -------------------------- RUN FLASK APP --------------------------
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
