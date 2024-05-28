from flask import session
import requests

from src.text_utilities import TextUtilities

utilities = TextUtilities()


class APIClient:
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers

    def make_request(self, payload):
        response = None
        try:
            session.modified = True
            """"   
            if payload == "answer":
                session["conversation"].append(
                    {
                        "message_type": "answer",
                        "text": "esta es una respuesta ",
                        "time": utilities.format_time(),
                    }
                )
            else:
                session["conversation"].append(
                    {
                        "message_type": "question",
                        "text": "esta es una pregunta ",
                        "time": utilities.format_time(),
                    }
                )
            """

            question_time = utilities.format_time()
            pregunta = {"in-0": payload, "user_id": """<USER or Conversation ID>"""}
            print(pregunta)
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=pregunta,
            )

            answer_time = utilities.format_time()
            response.raise_for_status()
            # create a new response object
            data = response.json()
            to_translate = data["outputs"]["out-0"]
            translated = utilities.translate_text(to_translate)

            if "conversation" not in session:
                session["conversation"] = []

            question = {
                "message_type": "question",
                "text": payload,
                "time": question_time,
            }
            session["conversation"].append(question)
            anwser = {
                "message_type": "answer",
                "text": translated,
                "time": answer_time,
            }
            session["conversation"].append(anwser)

            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Error en la solicitud a la API: {str(e)}"

            if response and response.status_code == 402:
                response_json = response.json()
                if "detail" in response_json:
                    error_message = response_json["detail"]
            print(error_message)
            return {
                "error": utilities.translate_text(error_message),
            }
