# import os
# from flask import Flask, request, redirect, url_for, render_template


import os
from scripts.resume_creator import ResumeCreator
from scripts.resume_parser import ResumeParser
from scripts.analyzer import DataAnalyzer
from scripts.job_parser import JobParser


if __name__ == '__main__':


    print("Welcome to the resume parser")
    print("Copy your resume to the Resumes folder and then enter the number of the resume you want to parse from the following list. If your resume is not in the list, please add it to the Resumes folder and then rerun the program.")
    resumes = os.listdir("./Resumes")
    for i in range(len(resumes)):
        print(f"{i+1}. {resumes[i]}")
    print(f"{len(resumes)+1}. Reload")
    option = int(input("Enter the number of the resume you want to parse: "))
    if option == len(resumes)+1:
        exit()
    resume = ResumeParser(f"./Resumes/{resumes[option-1]}")
    json = resume.generate_json()

    ResumeCreator().generate_pdf(json, "resume.pdf")

    analyzer = DataAnalyzer

    print(f"""Following details are extracted from the resume:
          Name: {json['name']}
          Email: {json['email']}
          Phone: {json['phone']}
          Linkedin URL: {json['url'][2]}
          Github URL: {json['url'][1]}"""
          )

    analyzer.resume_words_count_analyzer(json["count_of_words"])
    analyzer.analyze_resume_character_length(json["count_of_characters"])
    # analyzer.analyze_resume_sentence_length(json["count_of_sentences"])
    urls = analyzer.analyze_urls(json["url"])

    if urls[1] is None:
        # Your code here:
        print("Linkedin URL not found. Consider adding it to the resume")
        option = input("Do you want to add it? (y/n): ")
        if option == 'y':
            linkedin_url = input("Enter the linkedin URL: ")
            json["url"][2] = linkedin_url
            print("Linkedin URL added successfully")
    if  urls[0] is None:
        print("Github URL not found. Consider adding it to the resume")
        option = input("Do you want to add it? (y/n): ")
        if option == 'y':
            github_url = input("Enter the github URL: ")
            json["url"][1] = github_url
            print("Github URL added successfully")

    print(f" Your experience in years is: {json['years_experience'][1]}")
    print(f"Following are the top 10 words in the resume: {analyzer.top_ten_frequency(json['frequency_of_words'])}")
    print(f"Your resume has {json['count_of_keywords']} keywords")
    print(
        f"Following are the top 10 keywords in the resume: {analyzer.top_ten_frequency(json['frequency_of_keywords'])}"
    )
    print(f"Your resume has {json['count_of_stopwords']} stopwords")
    print(f"Following are the top 10 stopwords in the resume: {analyzer.top_ten_frequency(json['frequency_of_stopwords'])}")
    print(f"The ratio of keywords to stopwords is: {json['keywords_to_stopwords_ratio']}. The ideal ratio is 3:1")
    print(f"The ratio of keywords to words is: {json['keywords_to_words_ratio']}. Try to increase the ratio")
    print(f"Following are the other words found in the resume. These words either do not belong to the stopwords or the keywords or are misspelled. Consider changing the words if possible: {json['other_words']}")

    for key,experience in json["experience"].items():
        analyzer.experience_length(experience['description'])
        for point in experience['description']:
            if not analyzer.follows_pattern(point):
                while True:
                    print(f"Following bullet point is not as per the pattern: {point}")
                    rephrased = analyzer.rephrase_experience_point(point, experience)
                    if rephrased is None:
                        print("Sorry, the bullet point could not be rephrased. Would you like to retry or skip this bullet point? (retry/skip): ")
                        option = input()
                        if option == 'skip':
                            break
                        else:
                            continue
                    print(f"Rephrased bullet point: {rephrased}")
                    option = input("Do you want to update the bullet point? (y/n): ")
                    if option == 'y':
                        experience['description'][experience['description'].index(point)] = rephrased
                        print("Bullet point updated successfully")
                        break
                    else:
                        option = input("Do you want to rephrase the bullet point again? (y/n): ")
                        if option == 'n':
                            break

    for key, project in json["projects"].items():
        for point in project['description']:
            if not analyzer.follows_pattern(point):
                while True:
                    print(
                        f"Following project description is not as per the pattern: {point}"
                    )
                    rephrased = analyzer.rephrase_experience_point(point, project)
                    if rephrased is None:
                        print("Sorry, the project description could not be rephrased. Would you like to retry or skip this project? (retry/skip): ")
                        option = input()
                        if option == 'skip':
                            break
                        else:
                            continue
                    print(f"Rephrased project description: {rephrased}")
                    option = input("Do you want to update the project description? (y/n): ")
                    if option == 'y':
                        project["description"][
                            project["description"].index(point)
                        ] = rephrased
                        print("Project description updated successfully")
                        break
                    else:
                        option = input("Do you want to rephrase the project description again? (y/n): ")
                        if option == 'n':
                            break

    while True:
        print("Here is your entire resume in a json pretty format: ")
        for key, value in json.items():

            if key in ["name", "email", "phone", "url", "experience", "education", "projects", "skills"]:
                if key in ["experience", "education"]:
                    print(f"{key}:")
                    for key2, value2 in value.items():
                        print(f"{key2}: {value2}")
                else:
                    print(f"{key}: {value}")

        option = input("Do you want to update any section of the resume? (y/n): ")
        if option == 'y':
            print("Following are the sections of the resume: ")
            for key in [
                "name",
                "email",
                "phone",
                "url",
                "experience",
                "education",
                "projects",
                "skills",
            ]:
                print(key)

            section = input("Enter the section you want to update: ")

            if section == "skills":
                option = input("Do you want to add, delete or update the skills? (add/delete/update): ")
                if option == "add":
                    new_skill = input("Enter the new skill: ")
                    json[section].append(new_skill)
                    print("Skill added successfully")
                elif option == "delete":
                    print(f"Following is the current content of the section: {json[section]}")
                    skill = input("Enter the skill you want to delete: ")
                    json[section].remove(skill)
                    print("Skill deleted successfully")
                elif option == "update":
                    print(f"Following is the current content of the section: {json[section]}")
                    new_skill = input("Enter the new skill: ")
                    skill = input("Enter the skill you want to update: ")
                    json[section][json[section].index(skill)] = new_skill
                    print("Skill updated successfully")
            # if section in json.keys():
            #     print(f"Following is the current content of the section: {json[section]}")
            #     new_content = input("Enter the new content: ")
            #     json[section] = new_content
            #     print("Section updated successfully")
            else:
                print("Invalid section. Please enter a valid section")
        else:
            break

    option = input("Do you want to generate a resume in a different format? (y/n): ")
    if option == 'y':
        format = input("Enter the format you want to generate the resume in (pdf/docx/html/markdown): ")
        name = input("Enter the name of the resume: ")
        resumeCreator = ResumeCreator()
        if format == "pdf":
            resumeCreator.generate_pdf(json, name)
        elif format == "docx":
            resumeCreator.generate_docx(json, name)
        elif format == "html":
            resumeCreator.generate_html(json, name)
        elif format == "markdown":
            resumeCreator.generate_markdown(json, name)
        print(f"{name} generated successfully")
        print("Thank you for using the resume parser")
    else:
        print("Thank you for using the resume parser")
