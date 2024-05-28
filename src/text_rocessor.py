class TextProcessor:
    def __init__(self, data):
        self.data = data

    def process_text(self):
        texto_sin_citations = ""
        texto_citations = ""
        text = self.data["outputs"]["out-0"]

        if "<citations>" in text and "</citations>" in text:
            texto_sin_citations = text.split("<citations>")[0].strip()
            texto_citations = "Tiene citas"
            """texto_citations = (
                text.split("<citations>")[1].split("</citations>")[0].strip()
            )"""
        else:
            texto_sin_citations = text.strip()
            texto_citations = ""

        return {
            "response": self._remove_html_tags(texto_sin_citations),
            "citations": self._remove_html_tags(texto_citations),
        }

    def _remove_html_tags(self, text):
        import re

        texto_limpio = re.sub(r"\[\^[0-9]+\.[0-9]+\.[0-9]+\]", "", text).strip()
        return texto_limpio
