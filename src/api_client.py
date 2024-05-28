import os
from flask import session
import requests
from dotenv import load_dotenv

from src.text_utilities import TextUtilities
from src.text_rocessor import TextProcessor

utilities = TextUtilities()


class ApiClient:
    def __init__(self):
        self.api_url = os.getenv("API_URL2")
        self.headers = {
            "Authorization": os.getenv("TOKEN_API"),
            "Content-Type": "application/json",
        }

    def make_request(self, payload):
        response = None
        try:
            session.modified = True

            question_time = utilities.format_time()
            response = self._send_request(payload)

            response.raise_for_status()
            textProcessor = TextProcessor(response.json())
            data = textProcessor.process_text()
            print(data)
            translated = utilities.translate_text(data["response"])

            self._update_session_conversation(
                payload, question_time, translated, data["citations"]
            )

            return data
        except requests.exceptions.RequestException as e:
            return self._handle_request_exception(
                e,
                response,
                payload,
                question_time,
            )

    def _send_request(self, payload):
        question_payload = {
            "in-0": payload,
            "user_id": """<USER or Conversation ID>""",
        }
        return requests.post(self.api_url, headers=self.headers, json=question_payload)

    def _update_session_conversation(
        self, payload, question_time, answer, citations=None
    ):
        answer_time = utilities.format_time()
        if "conversation" not in session:
            session["conversation"] = []

        question = self._new_data_session_conversation(
            "question", payload, question_time, citations
        )
        session["conversation"].append(question)

        answer = self._new_data_session_conversation("answer", answer, answer_time)
        session["conversation"].append(answer)

    def _new_data_session_conversation(self, message_type, text, time, citations=None):
        return {
            "message_type": message_type,
            "text": text,
            "time": time,
            "citations": citations,
        }

    def _handle_request_exception(
        self,
        exception,
        response,
        payload,
        question_time,
    ):
        error_message = f"Error en la solicitud a la API: {str(exception)}"
        error_time = utilities.format_time()

        if response and response.status_code == 402:
            response_json = response.json()
            if "detail" in response_json:
                error_message = response_json["detail"]

        if "errors" not in session:
            session["errors"] = []

        session["errors"].append(
            {
                "message": utilities.translate_text(error_message),
                "time": error_time,
            }
        )
        return self._get_fallback_response(payload, question_time)

    def _get_fallback_response(self, payload, question_time):
        # TODO: Implementar un mecanismo de fallback solicitar a clase de NLP que responde segun intenciones
        answer = "No pude contestar a tu pregunta, por favor intenta de nuevo."
        self._update_session_conversation(payload, question_time, answer)
        return True
