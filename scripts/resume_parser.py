import os
from pypdf import PdfReader
from scripts.extractor import DataExtractor

class ResumeParser:
    def __init__(self, input_file) -> None:
        input_file_name = os.path.join(input_file)
        resume_content_raw = self.__read_resume(input_file_name)
        self.__extractor = DataExtractor(resume_content_raw)

    def __read_resume(self, file_name):
        output = []
        with open(file_name, "rb") as f:
            pdf_reader = PdfReader(f)
            count = len(pdf_reader.pages)
            for i in range(count):
                page = pdf_reader.pages[i]
                output.append(page.extract_text())
        return str(" ".join(output))

    def generate_json(self):
        resume_json = {
            "name": self.__extractor.extract_name(),
            "email": self.__extractor.extract_email(),
            "phone": self.__extractor.extract_phone_number(),
            "url": self.__extractor.extract_urls(),
            "experience": self.__extractor.extract_experiences(),
            "education": self.__extractor.extract_education(),
            "summary": self.__extractor.extract_summary(),
            "projects": self.__extractor.extract_projects(),  # todo
            "skills": self.__extractor.extract_skills_section(),
            "years_experience": self.__extractor.extract_years_of_experience(),
            "frequency_of_words": self.__extractor.frequency_of_words(),
            "frequency_of_verbs": self.__extractor.frequency_of_verbs(),
            "frequency_of_adjectives": self.__extractor.frequency_of_adjectives(),
            # "skills_count": self.__extractor.skills_count(),  # to fix
            "count_of_sentences": self.__extractor.count_of_sentences(),
            "count_of_words": self.__extractor.count_of_words(),
            "count_of_characters": self.__extractor.count_of_characters(),
            "count_of_keywords": self.__extractor.count_of_keywords(),
            "count_of_stopwords": self.__extractor.count_of_stop_words(),
            "count_of_punctuations": self.__extractor.count_of_punctuations(),
            "keywords_to_stopwords_ratio": self.__extractor.keywords_to_stop_words_ratio(),
            "keywords_to_words_ratio": self.__extractor.keywords_to_words_ratio(),  # todo
            "stopwords_to_words_ratio": self.__extractor.words_to_stop_words_ratio(),  # todo
            "other_words": self.__extractor.extract_other_words(),  # todo
            "bigrams": self.__extractor.extract_bigrams(),  
            "trigrams": self.__extractor.extract_trigrams(),  
            "fourgrams": self.__extractor.extract_fourgrams(),  
            "frequency_of_bigrams": self.__extractor.frequency_of_bigrams(),
            "frequency_of_trigrams": self.__extractor.frequency_of_trigrams(),  
            "frequency_of_fourgrams": self.__extractor.frequency_of_fourgrams(),
            "keywords": self.__extractor.extract_keywords(),
            "frequency_of_keywords": self.__extractor.frequency_of_keywords(),
            "frequency_of_stopwords": self.__extractor.frequency_of_stop_words(),
            "extract_stopwords": self.__extractor.extract_stop_words(),
        }
        return resume_json
