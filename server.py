from flask import Flask, request, jsonify
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

client = MongoClient("mongodb+srv://hariomsolar:hariom123@cluster0.578ty4a.mongodb.net/")
db = client["hariomsolar"]
collection = db["career_applications"]

print("MongoDB Connected")


# ===============================
# Check Allowed File
# ===============================

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ===============================
# Apply API
# ===============================

@app.route("/apply", methods=["POST"])
def apply():
    try:

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        position = request.form.get("position")

        resume = request.files.get("resume")

        resume_path = ""

        if resume and allowed_file(resume.filename):

            filename = secure_filename(resume.filename)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            resume.save(filepath)

            resume_path = filepath

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "position": position,
            "resume": resume_path
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
# Home
# ===============================

@app.route("/")
def home():
    return "Hariom Solar API Running"



    # ===============================
# ADMIN API (GET ALL APPLICATIONS)
# ===============================
@app.route("/applications", methods=["GET"])
def get_applications():

    apps = []

    for app_data in collection.find():
        app_data["_id"] = str(app_data["_id"])
        apps.append(app_data)

    return jsonify(apps)


# ===============================
# DOWNLOAD RESUME
# ===============================
@app.route('/resume/<filename>')
def download_resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)


# ===============================
# Run Server
# ===============================

if __name__ == "__main__":
    app.run(port=5000, debug=True)