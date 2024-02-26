from ast import Constant
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk import CFG, ChartParser
import spacy

from scripts.constants import EXPERIENCE_BULLET_PROMPT, nlp
from scripts.generativeai import GenerativeAI




class DataAnalyzer:

    def plot_keywords_to_stopwords_ratio(ratio):
        color = "green" if ratio >= 3 and ratio <= 5 else "red"

        # Plot the bar chart
        plt.bar("Ratio", ratio, color=color)
        plt.axhline(y=3, color="gray", linestyle="--", label="Ideal Ratio")
        plt.xlabel("Name")
        plt.ylabel("Keywords to stopwords ratio")
        plt.title("Keywords to stopwords ratio of the resume")
        plt.ylim(0, 5)
        plt.legend()
        plt.show()

    def plot_word_cloud(data):

        wordcloud = WordCloud(
            width=800,
            height=400,
            random_state=21,
            max_font_size=110,
            background_color="white",
        ).generate_from_frequencies(data)
        plt.figure(figsize=(10, 7))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def plot_frequency_of_keywords(data):
        # Plot the bar chart
        sorted_word_freq = {
            k: v
            for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
        }

        plt.bar(sorted_word_freq.keys(), sorted_word_freq.values())
        plt.xlabel("Keywords")
        plt.ylabel("Frequency")
        plt.title("Frequency of keywords in the resume")
        plt.show()

    def compare_keywords(
        resume_keywords_frequency: dict, job_description_keywords_frequency: dict
    ):
        missing_keywords = []
        for keyword, frequency in job_description_keywords_frequency.items():
            if keyword not in resume_keywords_frequency.keys():
                missing_keywords.append((keyword, frequency))
        missing_keywords.sort(key=lambda x: x[1], reverse=True)
        return missing_keywords

    def analyze_resume_character_length(length: int):
        if length < 2000:
            print(f"The resume is too short {length} characters")
        elif length > 5000:
            print(f"The resume is too long {length} characters")
        else:
            print(f"The resume has an ideal character count of {length} characters")

    def follows_pattern(sentence):
        doc = nlp(sentence)
        pattern = ["VERB", "ADJ", "NOUN", "VERB", "NOUN"]
        pattern_index = 0
        if doc[0].pos_ != "VERB":
            return False
        if "NUM" not in [token.pos_ for token in doc]:
            return False
        for token in doc:
            if token.pos_ == pattern[pattern_index]:
                pattern_index += 1
                if pattern_index == len(pattern):
                    return True

        return False

    def plot_frequency_graph(data: dict, title: str, xlabel: str, ylabel: str):
        sorted_word_freq = {
            k: v
            for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
        }

        plt.bar(sorted_word_freq.keys(), sorted_word_freq.values())
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.show()

    def analyze_urls(urls: list):
        if len(urls) == 0:
            return None, None
        else:
            github_url = next((url for url in urls if "github" in url), None)
            linkedin_url = next((url for url in urls if "linkedin" in url), None)
            return github_url, linkedin_url

    def experience_length(points: list):
        if len(points) < 3:
            print("The resume lacks points")
        elif len(points) > 6:
            print("The resume has too much points")
        else:
            print(f"The resume has an ideal number of points {len(points)}")

    def rephrase_experience_point(point: str, context):
        # try:
        temp = f"""
        {EXPERIENCE_BULLET_PROMPT}
        Context of the point: {context}

        Original sentence: {point}"""
        model = GenerativeAI().model
        response = model.generate_content(EXPERIENCE_BULLET_PROMPT + " " + point)
        point = response.text
        return point
        # except:
        #     return None

    def rephrase_education_point(point: str):
        loop = 3
        while not DataAnalyzer.follows_pattern(point) and loop > 0:
            temp = f"""
            {EXPERIENCE_BULLET_PROMPT}

            Original sentence: {point}"""
            model = GenerativeAI().model
            response = model.generate_content(EXPERIENCE_BULLET_PROMPT + " " + point)
            point = response.text
            loop -= 1
        return point
    
    def resume_words_count_analyzer(count: int):
        if count < 300:
            print("The resume is too short {count}".format(count = count))
        elif count > 500:
            print("The resume is too long {count}".format(count = count) + " words")
        else:
            print("The resume has an ideal word count of {count}".format(count = count))
    
    def top_ten_frequency(data: dict):
        sorted_word_freq = {
            k: v
            for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
        }
        return [(word, freq) for word, freq in sorted_word_freq.items()][:10]


if __name__ == "__main__":
    pass
