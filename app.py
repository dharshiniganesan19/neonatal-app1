from flask import Flask, render_template, request, redirect, url_for, session, flash
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple authentication
        if username == "Dharshini"and password == "1234":
            session['user'] = username
            flash("✅ Login Successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid Username or Password", "danger")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template("dashboard.html", user=session['user'])
    flash("⚠️ Please login first", "warning")
    return redirect(url_for('login'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("👋 Logged out successfully", "info")
    return redirect(url_for('login'))


# ---------------- PREDICTION PAGE ----------------
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        flash("⚠️ Please login first", "warning")
        return redirect(url_for('login'))

    result = None
    color = ""
    emoji = ""

    if request.method == 'POST':
        try:
            # ---------------- INPUT DATA ----------------
            data = np.array([[ 
                float(request.form['mother_age']),
                0 if request.form['delivery_type'] == "normal" else 1,
                float(request.form['birth_weight']),
                0 if request.form['gender'] == "male" else 1,
                float(request.form['gestation_weeks']),
                float(request.form['blood_pressure']),
                float(request.form['heart_rate']),
                float(request.form['temperature'])
            ]])

            # ---------------- PREDICTION ----------------
            pred = model.predict(data)

            diseases = [
                "Healthy Baby",
                "Neonatal Sepsis",
                "Respiratory Distress",
                "Birth Asphyxia",
                "Jaundice",
                "Hypothermia",
                "Low Birth Weight"
            ]

            result = diseases[pred[0]]

            # ---------------- COLOR LOGIC ----------------
            if pred[0] == 0:
                color = "green"
                emoji = "✅"
            else:
                color = "red"
                emoji = "⚠️"

        except:
            result = "Invalid Input Data"
            color = "red"
            emoji = "❌"

    return render_template("index.html", result=result, color=color, emoji=emoji)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)