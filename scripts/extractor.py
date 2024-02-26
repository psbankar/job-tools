from collections import defaultdict
import re
from scripts.text_cleaner import TextCleaner
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
from nltk.corpus import stopwords
from datetime import datetime
from scripts.constants import RESUME_SECTIONS, JOB_TITLES, nlp
import pandas as pd
programming_languages_df = pd.read_csv("data/programming_languages.csv")
other_keywords_df = pd.read_csv("data/keywords.csv")

combined_df = pd.concat([programming_languages_df, other_keywords_df], ignore_index=True)

# pattern = re.compile(r"^[a-zA-Z0-9_\s\-,()&\.\/\+]+$")
# programming_languages = [
#     str(word).strip()
#     for word in programming_languages_df["skills"]
#     if pattern.match(str(word))
# ]


class DataExtractor:

    def __init__(self, text: str):
        self.__resume_content_raw = text
        clean_text = TextCleaner.remove_phone_emails_links(self.__resume_content_raw)
        self.__clean_text = TextCleaner.remove_unwanted_chars(clean_text)
        self.__clean_text = self.__clean_text.replace("\n", " ")
        self.__doc = nlp(self.__clean_text)

    def extract_name(self):
        name = self.__resume_content_raw.split("\n")[0].strip()
        return name

    def extract_email(self):
        try:
            email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            emails = re.findall(email_pattern, self.__resume_content_raw)
            return emails[0]
        except:
            return None

    def extract_phone_number(self):
        try:
            phone_number_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
            phone_numbers = re.findall(phone_number_pattern, self.__resume_content_raw)
            return phone_numbers[0]
        except:
            return None

    def extract_urls(self):
        url_pattern = (
            r"(([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?)"
        )
        urls = re.findall(url_pattern, self.__resume_content_raw)
        urls = [url[0] for url in urls if url[0] != ""]
        github_url = next((url for url in urls if "github" in url), None)
        linkedin_url = next((url for url in urls if "linkedin" in url), None)
        return urls, github_url, linkedin_url

    def extract_experiences(self):
        experience_section = []
        in_experience_section = False
        sentences = self.__resume_content_raw.split("\n")
        for sentence in sentences:
            if sentence.strip().lower() in RESUME_SECTIONS:
                if sentence.strip().lower() in [
                    "experience",
                    "work experience",
                    "professional experience",
                    "employment history",
                ]:
                    in_experience_section = True
                else:
                    in_experience_section = False

            if in_experience_section:
                experience_section.append(sentence.strip())
        if len(experience_section) == 0:
            return None
        experience_section.pop(0)
        separate_experience = {}

        date_regex = r"((([A-Za-z]+[.]{0,1})\s(\d{4}))\s[\-–]\s(([A-Za-z]+[.]{0,1})\s(\d{4})|(Present)))"
        text_before_date_regex = r"^(.*)\s" + date_regex
        location_regex = r"(([^,]+),\s*([^,]+)\b)"
        text_before_location_regex = r"^(.*)\s" + location_regex
        key = 1
        for exp in experience_section:
            exp = re.sub(r"\s+", " ", exp).strip()
            if re.match(text_before_date_regex, exp):

                split_strings = re.findall(text_before_date_regex, exp)
                if len(split_strings) != 0:
                    first_part = split_strings[0][0]
                    if any(element in JOB_TITLES for element in first_part.split()):
                        if key not in separate_experience.keys():
                            separate_experience[key] = {'job_title': first_part}
                        elif "job_title" not in separate_experience[key].keys():
                            separate_experience[key]['job_title'] = first_part
                        else:
                            key+=1
                            separate_experience[key] = {'job_title': first_part}

                    else:
                        if key not in separate_experience.keys():
                            separate_experience[key] = {'company': first_part}
                        elif "company" not in separate_experience[key].keys():
                            separate_experience[key]['company'] = first_part
                        else:
                            key+=1
                            separate_experience[key] = {'company': first_part}
                    if key not in separate_experience.keys():
                        separate_experience[key] = {'date': split_strings[0][1]}
                    elif "date" not in separate_experience[key].keys():
                        separate_experience[key]['date'] = split_strings[0][1]
                    else:
                        key+=1
                        separate_experience[key] = {'date': split_strings[0][1]
                    }
            elif re.match(location_regex, exp):
                split_strings = re.findall(text_before_location_regex, exp)
                if len(split_strings) != 0:
                    doc = nlp(split_strings[0][1])
                    location = None
                    for ent in doc.ents:
                        if ent.label_ == "GPE":
                            location = split_strings[0][1]
                    if location:
                        if key not in separate_experience.keys():
                            separate_experience[key] = {'location': location}
                        elif "location" not in separate_experience[key].keys():
                            separate_experience[key]['location'] = location
                        else:
                            key+=1
                            separate_experience[key] = {'location': location}
                        first_part = split_strings[0][0]
                        if any(element in JOB_TITLES for element in first_part.split()):
                            # key += 1
                            if key not in separate_experience.keys():
                                separate_experience[key] = {'job_title': first_part}
                            elif "job_title" not in separate_experience[key].keys():
                                separate_experience[key]['job_title'] = first_part
                            else:
                                key+=1
                                separate_experience[key] = {'job_title': first_part}
                        else:
                            if key not in separate_experience.keys():
                                separate_experience[key] = {'company': first_part}
                            elif "company" not in separate_experience[key].keys():
                                separate_experience[key]['company'] = first_part
                            else:
                                key+=1
                                separate_experience[key] = {'company': first_part}

                    else:
                        if key not in separate_experience.keys():
                            separate_experience[key] = {'description': [exp]}
                        else:
                            if "description" not in separate_experience[key].keys():
                                separate_experience[key]['description'] = [exp]
                            else:
                                separate_experience[key]['description'].append(exp)
            else:
                if len(exp) > 0:
                    if key not in separate_experience.keys():
                        separate_experience[key] = {'description': [exp]}
                    else:
                        if "description" not in separate_experience[key].keys():
                            separate_experience[key]['description'] = [exp]
                        else:
                            separate_experience[key]['description'].append(exp)

        for k,v in separate_experience.items():
            if "description" in v.keys():
                v["description"] = " ".join(v["description"])
                # symbols = ['.', ',', ';', ':', '?', '!']
                bullet_types = ["\u2022", "\u2023", "\u25E6", "\u2043", "\u2219", "\u25AA", "\u25CF", "\u25A0", "\u29BF", "\u25A1", "\u25AB", "\u25FD", "\u25FE", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9"]

                pattern = "|".join(re.escape(symbol) for symbol in bullet_types)
                parts = re.split(pattern, v['description'])
                parts = [part for part in parts if part]
                v['description'] = parts
        return separate_experience

    def extract_job_title(self, text):
        with open("data/titles_combined.txt", "r", encoding="utf-8") as f:
            job_titles = f.read().split("\n")
            job_titles = [title.lower() for title in job_titles]
            if text.lower() in job_titles:
                return text

    def get_stop_words(self):
        stop_words = set(stopwords.words("english"))
        return stop_words

    def extract_other_words(self):
        keywords = self.extract_keywords()
        stop_words = self.extract_stop_words()
        other_words = [
            token.text
            for token in self.__doc
            if token.text not in keywords and token.text not in stop_words and token.text.isalnum() and not token.pos_ == "VERB" and not token.pos_ == "ADJ"
        ]
        return other_words

    def extract_education(self):
        education_section = []
        in_education_section = False
        sentences = self.__resume_content_raw.split("\n")
        for token in sentences:
            if token.strip().lower() in RESUME_SECTIONS:
                if token.strip().lower() in [
                    "education",
                    "academic history",
                    "academic qualifications",
                    "academic background",
                    "educational background",
                ]:
                    in_education_section = True
                else:
                    in_education_section = False

            if in_education_section:
                education_section.append(token.strip())
        if len(education_section) == 0:
            return None
        education_section.pop(0)
        separate_education = {}
        location_regex = r"(([^,]+),\s*([^,]+)\b)"
        text_before_location_regex = r"^(.*)\s" + location_regex
        date_regex = r"((([A-Za-z]+[.]{0,1})\s(\d{4}))\s[\-–]\s(([A-Za-z]+[.]{0,1})\s(\d{4})|(Present)))"
        text_before_date_regex = r"^(.*)\s" + date_regex
        key = 1
        for exp in education_section:
            exp = re.sub(r"\s+", " ", exp).strip()

            if re.match(location_regex, exp):
                split_strings = re.findall(text_before_location_regex, exp)
                if len(split_strings) != 0:
                    doc = nlp(split_strings[0][1])
                    location = None
                    for ent in doc.ents:
                        if ent.label_ == "GPE":
                            location = split_strings[0][1]
                    if location:
                        if key not in separate_education.keys():
                            separate_education[key] = {'location': location}
                        elif "location" not in separate_education[key].keys():
                            separate_education[key]['location'] = location
                        else:
                            key+=1
                            separate_education[key] = {'location': location}
                        first_part = split_strings[0][0]
                        if key not in separate_education.keys():
                            separate_education[key] = {'university': first_part}
                        elif "university" not in separate_education[key].keys():
                            separate_education[key]['university'] = first_part
                        else:
                            key+=1
                            separate_education[key] = {'university': first_part}
                    else:
                        if key not in separate_education.keys():
                            separate_education[key] = {'description': [exp]}
                        else:
                            if "description" not in separate_education[key].keys():
                                separate_education[key]['description'] = [exp]
                            else:
                                separate_education[key]['description'].append(exp)

            elif re.match(text_before_date_regex, exp):
                split_strings = re.findall(text_before_date_regex, exp)
                if len(split_strings) != 0:
                    first_part = split_strings[0][0]
                    if key not in separate_education.keys():
                        separate_education[key] = {'degree': first_part}
                    elif "degree" not in separate_education[key].keys():
                        separate_education[key]['degree'] = first_part
                    else:
                        key+=1
                        separate_education[key] = {'degree': first_part}
                    if key not in separate_education.keys():
                        separate_education[key] = {'date': split_strings[0][1]}
                    elif "date" not in separate_education[key].keys():
                        separate_education[key]['date'] = split_strings[0][1]
                    else:
                        key+=1
                        separate_education[key] = {'date': split_strings[0][1]}
            else:
                if key not in separate_education.keys():
                    separate_education[key] = {'description': [exp]}
                else:
                    if "description" not in separate_education[key].keys():
                        separate_education[key]['description'] = [exp]
                    else:
                        separate_education[key]['description'].append(exp)

        return separate_education

    def extract_summary(self):
        summary_section = []
        in_summary_section = False
        sentences = self.__resume_content_raw.split("\n")
        for token in sentences:
            if token.strip().lower() in RESUME_SECTIONS:
                if token.strip().lower() in [
                    "summary",
                    "objective",
                    "career objective",
                    "career summary",
                ]:
                    in_summary_section = True
                else:
                    in_summary_section = False

            if in_summary_section:
                summary_section.append(token)
        if len(summary_section) == 0:
            return None
        summary_section.pop(0)
        summary_section = " ".join(summary_section)

        summary_section = re.sub(r"\s+", " ", summary_section).strip()
        return summary_section

    def extract_projects(self):
        projects_section = []
        in_projects_section = False
        sentences = self.__resume_content_raw.split("\n")
        for token in sentences:
            if token.strip().lower() in RESUME_SECTIONS:
                if token.strip().lower() in [
                    "projects",
                    "project experience",
                    "project history",
                    "project details",
                ]:
                    in_projects_section = True
                else:
                    in_projects_section = False

            if in_projects_section:
                projects_section.append(token)
        if len(projects_section) == 0:
            return None
        projects_section.pop(0)
        key = 1
        separate_projects = {}
        for exp in projects_section:
            exp = re.sub(r"\s+", " ", exp).strip()
            if "|" in exp:
                exp = exp.split("|")
                if key not in separate_projects.keys():
                    separate_projects[key] = {'name': exp[0]}
                else:
                    if "name" not in separate_projects[key].keys():
                        separate_projects[key]['name'] = exp[0]
                    else:
                        key+=1
                        separate_projects[key] = {'name': exp[0]}
                if key not in separate_projects.keys():
                    separate_projects[key] = {'technologies': [exp[1]]}
                else:
                    if "technologies" not in separate_projects[key].keys():
                        separate_projects[key]['technologies'] = [exp[1]]
                    else:
                        separate_projects[key]["technologies"].append(exp[1])

            else:
                if key not in separate_projects.keys():
                    separate_projects[key] = {'description': [exp]}
                else:
                    if "description" not in separate_projects[key].keys():
                        separate_projects[key]['description'] = [exp]
                    else:
                        separate_projects[key]['description'].append(exp)
            # if len(exp) > 0:
            #     if key not in separate_projects.keys():
            #         separate_projects[key] = {'description': [exp]}
            #     else:
            #         if "description" not in separate_projects[key].keys():
            #             separate_projects[key]['description'] = [exp]
            #         else:
            #             separate_projects[key]['description'].append(exp)
                        
        for k,v in separate_projects.items():
            if "description" in v.keys():
                v["description"] = " ".join(v["description"])
                bullet_types = ["\u2022", "\u2023", "\u25E6", "\u2043", "\u2219", "\u25AA", "\u25CF", "\u25A0", "\u29BF", "\u25A1", "\u25AB", "\u25FD", "\u25FE", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9", "\u25E6", "\u25EB", "\u25C6", "\u25C7", "\u25A1", "\u25A0", "\u25C7", "\u25C6", "\u25AA", "\u25CB", "\u25B8", "\u25B9", "\u25EB", "\u25FD", "\u25FE", "\u25CF", "\u29BF", "\u25B8", "\u25B9"]
                pattern = "|".join(re.escape(symbol) for symbol in bullet_types)
                parts = re.split(pattern, v['description'])
                parts = [part for part in parts if part]
                v['description'] = parts

        return separate_projects

    def extract_skills_section(self):
        skills_section = []
        in_skills_section = False
        sentences = self.__resume_content_raw.split("\n")
        for token in sentences:
            if token.strip().lower() in RESUME_SECTIONS:
                if token.strip().lower() in [
                    "skills",
                    "technical skills",
                    "professional skills",
                ]:
                    in_skills_section = True
                else:
                    in_skills_section = False

            if in_skills_section:
                skills_section.append(token.strip())
        if len(skills_section) == 0:
            return None
        skills_section.pop(0)
        all_skills = []
        for i in skills_section:
            i = i.split(":")
            if len(i) > 1:
                i = i[1]
            else:
                i = i[0]
            for skill in i.split(","):
                if len(skill) > 0:
                    all_skills.append(skill.strip())

        return all_skills

    def extract_years_of_experience(self):
        experience = self.extract_experiences()
        if experience is None:
            return 0, 0
        total_months, total_years = 0, 0
        position_year_search_pattern = r"((([A-Za-z]+[.]{0,1})\s(\d{4}))\s[\-–]\s(([A-Za-z]+[.]{0,1})\s(\d{4})|(Present)))"
        month_map = {
            "jan": 1,
            "january": 1,
            "feb": 2,
            "february": 2,
            "mar": 3,
            "march": 3,
            "apr": 4,
            "april": 4,
            "may": 5,
            "jun": 6,
            "june": 6,
            "jul": 7,
            "july": 7,
            "aug": 8,
            "august": 8,
            "sep": 9,
            "sept": 9,
            "september": 9,
            "oct": 10,
            "october": 10,
            "nov": 11,
            "november": 11,
            "dec": 12,
            "december": 12,
        }

        for k,v in experience.items():
            position_year = v['date']
            position_year = re.findall(position_year_search_pattern, position_year)
            if position_year:
                start_month, start_year, end_month, end_year = position_year[0][2], position_year[0][3], position_year[0][5], position_year[0][6]
                if position_year[0][7].lower() == "present":
                    now = datetime.now()
                    end_month = now.month
                    end_year = now.year

                start_month_num = month_map.get(start_month.lower(), None)
                if type(end_month) == str:
                    end_month_num = month_map.get(end_month.lower(), None)
                else:
                    end_month_num = end_month

                # Validate input
                if start_month_num is None or end_month_num is None:
                    raise ValueError("Invalid month name")

                start_date = datetime(int(start_year), start_month_num, 1)
                end_date = datetime(int(end_year), end_month_num, 1)

                # Calculate difference
                if start_date > end_date:
                    raise ValueError("Start date cannot be after end date")

                total_months += (end_date.year - start_date.year) * 12 + (
                    end_date.month - start_date.month
                )
                total_years += total_months // 12

        return total_months, total_years

    def frequency_of_words(self):
        word_freq = defaultdict(int)
        word_toknized = word_tokenize(self.__clean_text)
        for word in word_toknized:
            if word.isalnum():
                word_freq[word.lower()] += 1
        return dict(word_freq)

    def count_of_keywords(self):
        keywords = self.extract_keywords()
        return len(keywords)

    def frequency_of_stop_words(self):
        stopword_freq = {}
        stop_words = self.extract_stop_words()
        for word in stop_words:
            if word.lower() not in stopword_freq:
                stopword_freq[word.lower()] = 1
            else:
                stopword_freq[word.lower()] += 1

        return stopword_freq

    def frequency_of_verbs(self):
        verbs = defaultdict(int)
        doc = nlp(self.__clean_text)
        for token in doc:
            if token.pos_ == "VERB":
                verbs[token.lemma_] += 1
        return dict(verbs)

    def frequency_of_adjectives(self):
        adjectives = defaultdict(int)
        for token in self.__doc:
            if token.pos_ == "ADJ":
                adjectives[token.text] += 1
        return adjectives

    def frequency_of_pronouns(self):
        pronouns = defaultdict(int)
        for token in self.__doc:
            if token.pos_ == "PRON":
                pronouns[token.text] += 1
        return pronouns

    def frequency_of_keywords(self):
        keywords = self.extract_keywords()
        keyword_freq = {}
        for word in keywords:
            if word.lower() not in keyword_freq:
                keyword_freq[word.lower()] = 1
            else:
                keyword_freq[word.lower()] += 1
        return keyword_freq

    def count_of_stop_words(self):
        return len(self.extract_stop_words())

    def extract_stop_words(self):
        stop_words = self.get_stop_words()
        return [token.text for token in self.__doc if token.text.lower() in stop_words]

    def keywords_to_stop_words_ratio(self):
        keywords = self.count_of_keywords()
        stop_words = self.count_of_stop_words()
        return keywords / stop_words

    # def skills_count(self):
    #     skills = self.extract_skills_section()
    #     temp = []
    #     for skill in skills:
    #         temp.extend(skill.split(","))
    #     return len(temp)

    def count_of_sentences(self):
        return sum(1 for _ in self.__doc.sents)

    def count_of_words(self):
        return len(
            [token for token in word_tokenize(self.__clean_text) if token.isalnum()]
        )

    def count_of_characters(self):
        return len([char for char in self.__resume_content_raw if char.isalnum()])

    def count_of_punctuations(self):
        return len([token.text for token in self.__doc if token.is_punct])

    def count_of_digits(self):
        return len([token.text for token in self.__doc if token.is_digit])

    def keywords_to_words_ratio(self):
        keywords = self.extract_keywords()
        return len(keywords) / len([token.text for token in self.__doc if token.is_alpha])

    def words_to_stop_words_ratio(self):
        return self.count_of_words() / self.count_of_stop_words()

    def extract_bigrams(self):
        bigrams = []
        stop_words = self.get_stop_words()
        for token1, token2 in zip(self.__doc[:-1], self.__doc[1:]):
            if all(
                token.text.lower() not in stop_words
                and token.text.isalnum()
                and not token.is_punct
                for token in (token1, token2)
            ):
                bigrams.append((token1.text, token2.text))
        return bigrams

    def extract_trigrams(self):
        trigrams = []
        stop_words = self.get_stop_words()
        for token1, token2, token3 in zip(self.__doc[:-2], self.__doc[1:-1], self.__doc[2:]):
            if all(
                token.text.lower() not in stop_words
                and token.text.isalnum()
                and not token.is_punct
                for token in (token1, token2, token3)
            ):
                trigrams.append((token1.text, token2.text, token3.text))
        return trigrams

    def extract_fourgrams(self):
        fourgrams = []
        stop_words = self.get_stop_words()
        for token1, token2, token3, token4 in zip(self.__doc[:-3], self.__doc[1:-2], self.__doc[2:-1], self.__doc[3:]):
            if all(
                token.text.lower() not in stop_words
                and token.text.isalnum()
                and not token.is_punct
                for token in (token1, token2, token3, token4)
            ):
                fourgrams.append((token1.text, token2.text, token3.text, token4.text))
        return fourgrams

    def extract_keywords(self):
        stop_words = self.get_stop_words()
        keywords = [
            token.text for token in self.__doc if token.text.lower() not in stop_words and not token.is_punct and token.text.lower() in combined_df["skills"].values
        ]
        keywords.extend(
            [
                " ".join(token)
                for token in self.extract_bigrams()
                if " ".join(token).lower() in combined_df["skills"].values
            ]
        )
        keywords.extend(
            [
                " ".join(token)
                for token in self.extract_trigrams()
                if " ".join(token).lower() in combined_df["skills"].values

            ]
        )
        keywords.extend(
            [
                " ".join(token)
                for token in self.extract_fourgrams()
                if " ".join(token).lower() in combined_df["skills"].values
            ]
        )
        return keywords

    def frequency_of_bigrams(self):
        bigrams = self.extract_bigrams()
        bigram_freq = {}
        for bigram in bigrams:
            if bigram not in bigram_freq:
                bigram_freq[bigram] = 1
            else:
                bigram_freq[bigram] += 1
        return bigram_freq

    def frequency_of_trigrams(self):
        trigrams = self.extract_trigrams()
        trigram_freq = {}
        for trigram in trigrams:
            if trigram not in trigram_freq:
                trigram_freq[trigram] = 1
            else:
                trigram_freq[trigram] += 1
        return trigram_freq

    def frequency_of_fourgrams(self):
        fourgrams = self.extract_fourgrams()
        fourgram_freq = {}
        for fourgram in fourgrams:
            if fourgram not in fourgram_freq:
                fourgram_freq[fourgram] = 1
            else:
                fourgram_freq[fourgram] += 1
        return fourgram_freq
