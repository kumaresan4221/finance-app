from flask import Flask, render_template, request, redirect, session, flash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'rasappaaa123'

# 🧠 Local DB (dictionary)
users = {}

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['user'] = email
            return redirect('/home')
        else:
            flash("Invalid credentials!", "danger")
    return render_template('main.html', page='login', page_title="Login")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash("User already exists!", "danger")
        else:
            users[email] = password
            flash("Registration successful! Please login.", "success")
            return redirect('/login')
    return render_template('main.html', page='register', page_title="Register")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect('/login')

    today = datetime.now().strftime("%d-%m-%Y")
    month_file = datetime.now().strftime("%B-%Y") + ".xlsx"

    if os.path.exists(month_file):
        df = pd.read_excel(month_file)
    else:
        df = pd.DataFrame(columns=["Reg No", "Name", "Initial Due", "Remaining Due", "Last Updated"])

    if request.method == 'POST':
        reg = request.form['reg']
        name = request.form['name']
        due = float(request.form['due'])

        if reg in df["Reg No"].values:
            df.loc[df["Reg No"] == reg, "Remaining Due"] += due
            df.loc[df["Reg No"] == reg, "Last Updated"] = today
        else:
            df.loc[len(df)] = [reg, name, due, due, today]

        df.to_excel(month_file, index=False)
        flash("Customer data updated.", "success")
        return redirect('/home')

    return render_template("main.html", page='home', page_title='Dashboard',
                           data=df.to_dict(orient='records'), user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!", "info")
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
