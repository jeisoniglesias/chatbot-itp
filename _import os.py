import os
from datetime import datetime
import requests
from deep_translator import GoogleTranslator
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

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


def format_time(dt):
    return dt.strftime("%I:%M %p").lstrip("0").replace("AM", "am").replace("PM", "pm")


def translate_text(text):
    return GoogleTranslator(source="auto", target="es").translate(text)


def query(payload):
    headers = {
        "Authorization": os.getenv("TOKEN_API"),
        "Content-Type": "application/json",
    }
    response = requests.post(os.getenv("API_URL"), headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 402:
        detail = response.json()["detail"]
        return {"error": translate_text(detail), "code": response.status_code}
    else:
        return {
            "error": "Ocurrio un error inesperado, por favor intenta de nuevo mas tarde :(",
            "code": 404,
        }


def response(payload):
    question_time = datetime.now()
    output = query({"in-0": payload, "user_id": """2"""})
    if "error" in output:
        return output
    to_translate = output["outputs"]["out-0"]
    translated = translate_text(to_translate)
    answer_time = datetime.now()
    if "chat_history" not in session:
        session["chat_history"] = []
    session["chat_history"].append(
        {
            "message_type": "question",
            "text": payload,
            "time": format_time(question_time),
        }
    )
    session["chat_history"].append(
        {"message_type": "answer", "text": translated, "time": format_time(answer_time)}
    )
    session.modified = True
    return translated


@app.route("/", methods=["GET", "POST"])
def index():
    error_present = False
    messages = []
    chat_history=[]
    if get_flashed_messages(with_categories=True):
        messages = get_flashed_messages(with_categories=True)
    print("messages")
    print(messages)
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input.strip():
            result = response(user_input)
            if "error" in result:
                flash(result.get("error"), "alert-danger")
                error_present = True
                return redirect(url_for("error", error_message=result.get("error")))
            
        chat_history = session.get("chat_history", [])
        return render_template(
            "index.html",
            chat_history=chat_history,
            messages=messages,
            error_present=error_present,
        )

    return render_template(
        "index.html", chat_history=[], messages=messages, error_present=False
    )


@app.route("/error")
def error():
    error_message = request.args.get("error_message", "An unknown error occurred.")
    return render_template("error.html", error_message=error_message)


@app.route("/clear_session", methods=["POST"])
def clear_session():
    session.pop("chat_history", None)
    session.pop("_flashes", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
