from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import pandas as pd
import os
import pyrebase

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# 🔥 Firebase config
firebase_config = {
    "apiKey": "AIzaSyAy8oWoafy7D4dmRteUTbSiwi2cgvv2R0o",
    "authDomain": "finance-c2952.firebaseapp.com",
    "databaseURL": "https://finance-c2952-default-rtdb.firebaseio.com",
    "projectId": "finance-c2952",
    "storageBucket": "finance-c2952.appspot.com",
    "messagingSenderId": "930628148516",
    "appId": "1:930628148516:web:ba21b485b0fc40831c67b1",
    "measurementId": "G-5XNK4YTRD2"
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# 📅 Helper to get today's date string
def today_str():
    return datetime.now().strftime("%Y-%m-%d")

# 📁 Excel file path (saved by day)
def get_excel_path():
    return f"data_{today_str()}.xlsx"

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/register', methods=["POST"])
def register():
    name = request.form['name']
    regno = request.form['regno']
    amount = float(request.form['amount'])

    # Save to Firebase
    db.child("users").child(regno).set({
        "name": name,
        "regno": regno,
        "amount": amount,
        "date": today_str()
    })

    # Save to Excel
    excel_path = get_excel_path()
    new_data = {"Name": name, "RegNo": regno, "Amount": amount, "Date": today_str()}
    
    if os.path.exists(excel_path):
        df = pd.read_excel(excel_path)
        df = df.append(new_data, ignore_index=True)
    else:
        df = pd.DataFrame([new_data])
    
    df.to_excel(excel_path, index=False)
    flash("Customer registered and data saved ✅")
    return redirect(url_for("index"))

@app.route('/data')
def view_data():
    users = db.child("users").get().val()
    return users if users else {}

# ✅ For Render — expose port 0.0.0.0
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
