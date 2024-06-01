from deep_translator import GoogleTranslator

from datetime import datetime


class TextUtilities:
    def format_time(self):
        current_time = datetime.now()

        return (
            current_time.strftime("%I:%M %p")
            .lstrip("0")
            .replace("AM", "am")
            .replace("PM", "pm")
        )

    def translate_text(self, text):
        return GoogleTranslator(source="auto", target="es").translate(text)

    def response_chat(self, text):
        texto = GoogleTranslator(source="auto", target="en").translate(text)
        return self.translate_text(texto)

    def __init__(self):
        print("Utils class created")
