import json
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, render_template, request, redirect, url_for, flash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "devops-lab-mid-secret-key"

    project_dir = Path(__file__).resolve().parent.parent
    data_dir = project_dir / "data"
    data_dir.mkdir(exist_ok=True)

    app.config["DATA_FILE"] = data_dir / "submissions.json"

    if test_config:
        app.config.update(test_config)

    def load_submissions():
        file_path = Path(app.config["DATA_FILE"])

        if not file_path.exists():
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save_submissions(submissions):
        file_path = Path(app.config["DATA_FILE"])
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(submissions, file, indent=4)

    def is_valid_url(url):
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ("http", "https")
                and bool(parsed.netloc)
                and "." in parsed.netloc
                and " " not in url
            )
        except ValueError:
            return False

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            registration_number = request.form.get(
                "registration_number", ""
            ).strip()
            assignment_title = request.form.get(
                "assignment_title", ""
            ).strip()
            submission_url = request.form.get(
                "submission_url", ""
            ).strip()

            if not all([
                name,
                registration_number,
                assignment_title,
                submission_url
            ]):
                flash("All fields are required.", "error")
                return redirect(url_for("index"))

            if not is_valid_url(submission_url):
                flash(
                    "Invalid submission URL. Enter a valid HTTP or HTTPS URL.",
                    "error"
                )
                return redirect(url_for("index"))

            submissions = load_submissions()

            new_submission = {
                "name": name,
                "registration_number": registration_number,
                "assignment_title": assignment_title,
                "submission_url": submission_url
            }

            submissions.append(new_submission)
            save_submissions(submissions)

            flash("Assignment submitted successfully!", "success")
            return redirect(url_for("index"))

        submissions = load_submissions()
        return render_template(
            "index.html",
            submissions=submissions
        )

    return app
