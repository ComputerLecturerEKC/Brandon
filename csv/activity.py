from datetime import date
from flask import Flask, request, abort

from werkzeug.security import generate_password_hash

app = Flask(__name__)

def age_on(dob: date, today: date) -> int:
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

@app.post("/signup")
def signup():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    consent = request.form.get("consent") == "on"
    try:
        dob = date.fromisoformat(request.form.get("dob", ""))
    except ValueError:
        abort(400, "Enter a valid date of birth")

    age = age_on(dob, date.today())
    if not (3 <= len(username) <= 20) or len(password) < 12 or not consent:
        abort(400, "Check username, password length and consent box")
    if age < 13:
        abort(403, "Parent or carer consent needed")

    record = {
        "username": username,
        "password_hash": generate_password_hash(password),
        "age_band": "13-15" if age < 16 else "16+",
        # DOB deliberately not stored (data minimisation)
    }
    # save record to database here
    return "Account created", 201
