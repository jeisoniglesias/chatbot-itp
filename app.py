import os
import requests
from flask import (
    Flask,
    get_flashed_messages,
    render_template,
    session,
    request,
    redirect,
    url_for,
    flash,
)

from src.api_client import ApiClient

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


@app.route("/", methods=["GET", "POST"])
def index():
    conversation = session.get("conversation", [])
    follow_up = session.get("follow_up", [])
    return render_template(
        "pages/index.html",
        conversation=conversation,
        follow_up=follow_up,
        messages=session.get("messages", []),
    )


@app.route("/error")
def error():
    error_message = session.get("error_message", "Ha ocurrido un error desconocido.")
    return render_template("pages/error.html", error_message=error_message)


@app.route("/clear_session", methods=["POST"])
def clear_session():
    print("clear session")
    session.pop("conversation", None)
    session.pop("error_message", None)
    return redirect(url_for("index"))


@app.route("/answer", methods=["POST"])
def answer():
    payload = request.form.get("payload")
    if not payload.strip():
        return redirect(url_for("index"))
    api_client = ApiClient()
    response_data = api_client.make_request(payload)
    """
    if "error" in response_data:
        error_message = response_data["error"]
        session["error_message"] = error_message
        return redirect(url_for("error"))
    """
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
