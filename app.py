from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# =========================
# CONFIGURATION
# =========================

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# MONGODB CONNECTION
# =========================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://hariomsolar:hariom123@cluster0.578ty4a.mongodb.net/hariomsolar?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI)

db = client["hariomsolar"]
collection = db["career_applications"]

# =========================
# FILE VALIDATION FUNCTION
# =========================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =========================
# HOME PAGE
# =========================

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# =========================
# CAREERS PAGE
# =========================

@app.route("/careers")
def careers():
    return send_from_directory(".", "careers.html")


# =========================
# STATIC FILES
# =========================

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# =========================
# JOB APPLICATION API
# =========================

@app.route("/apply", methods=["POST"])
def apply():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    position = request.form.get("position")

    resume = request.files.get("resume")
    filename = None

    if resume and resume.filename != "":

        if allowed_file(resume.filename):

            filename = secure_filename(resume.filename)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            resume.save(filepath)

        else:
            return jsonify({
                "success": False,
                "message": "Invalid file type. Only PDF, DOC, DOCX allowed."
            })

    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "position": position,
        "resume_file": filename
    }

    collection.insert_one(data)

    return jsonify({
        "success": True,
        "message": "Application submitted successfully"
    })


# =========================
# CONTACT API
# =========================

@app.route("/api/contact", methods=["POST"])
def contact():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    print("Contact Message:", data)

    return jsonify({
        "success": True,
        "message": "Message received!"
    })


# =========================
# QUOTE API
# =========================

@app.route("/api/quote", methods=["POST"])
def quote():

    data = request.get_json()

    print("Quote Request:", data)

    return jsonify({
        "success": True
    })


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    print("=" * 50)
    print("Hariom Solar Server Running")
    print("Open: http://localhost:5000")
    print("=" * 50)

    app.run(debug=True)