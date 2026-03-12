from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# ===============================
# Upload Folder
# ===============================
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# ===============================
# MongoDB Connection
# ===============================
client = MongoClient("mongodb+srv://hariomsolar:hariom123@cluster0.578ty4a.mongodb.net/hariomsolar?retryWrites=true&w=majority")

db = client["hariomsolar"]
collection = db["career_applications"]

print("✅ MongoDB Connected")


# ===============================
# Check Allowed File
# ===============================
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ===============================
# APPLY API
# ===============================
@app.route("/apply", methods=["POST"])
def apply():
    try:

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        position = request.form.get("position")

        resume = request.files.get("resume")

        resume_filename = ""

        if resume and allowed_file(resume.filename):

            filename = secure_filename(resume.filename)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            resume.save(filepath)

            resume_filename = filename

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "position": position,
            "resume": resume_filename
        }

        collection.insert_one(data)

        return jsonify({
            "status": "success",
            "message": "Application submitted successfully"
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ===============================
# ADMIN API (GET APPLICATIONS)
# ===============================
@app.route("/applications", methods=["GET"])
def get_applications():

    applications = []

    for app_data in collection.find():

        app_data["_id"] = str(app_data["_id"])
        applications.append(app_data)

    return jsonify(applications)


# ===============================
# DOWNLOAD RESUME
# ===============================
@app.route("/resume/<filename>")
def download_resume(filename):

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


# ===============================
# HOME API
# ===============================
@app.route("/")
def home():
    return "🚀 Hariom Solar API Running"


# ===============================
# RUN SERVER
# ===============================
if __name__ == "__main__":
    app.run(port=5000, debug=True)