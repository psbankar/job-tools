# from uuid import uuid4
import base64
from io import BytesIO
import re

REGEX_PATTERNS = {
    "email_pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone_pattern": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    "link_pattern": r"([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?",
}



class TextCleaner:
    def remove_phone_emails_links(text):

        for pattern in REGEX_PATTERNS:
            text = re.sub(REGEX_PATTERNS[pattern], "", text)
        return text

    def remove_unwanted_chars(text):
        """
        Clean the input text by removing unwanted characters.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """

        text = re.sub(r"[^a-zA-Z0-9_\s\-,()&\.\/\+]", "", text)
        return text
    

#     def clean_text(text):
#         """
#         Clean the input text by removing specific patterns.

#         Args:
#             text (str): The input text to clean.

#         Returns:
#             str: The cleaned text.
#         """
#         text = TextCleaner.remove_phone_emails_links(text)
#         doc = nlp(text)
#         for token in doc:
#             if token.pos_ == "PUNCT":
#                 text = text.replace(token.text, "")
#         return str(text)

#     def remove_stopwords(text):
#         """
#         Clean the input text by removing stopwords.

#         Args:
#             text (str): The input text to clean.

#         Returns:
#             str: The cleaned text.
#         """
#         doc = nlp(text)
#         for token in doc:
#             if token.is_stop:
#                 text = text.replace(token.text, "")
#         return text
