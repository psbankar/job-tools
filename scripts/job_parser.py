import requests
from bs4 import BeautifulSoup
import re
from scripts.extractor import DataExtractor

class JobParser:

    def fetch_job_details_from_linkedin_url(self, url):
        if "currentJobId" in url:
            jobId = re.search(r'currentJobId=(\d+)', url).group(1)
            url = f"https://www.linkedin.com/jobs/view/{jobId}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        job_title = soup.find("h1", class_="topcard__title").text
        # Find the organization name element (try both selectors)
        organization_element = soup.find("span", {"class": "topcard__flavor"})

        if not organization_element:
            organization_element = soup.find("a", {"class": "topcard__org-name-link"})

        # Extract the organization name
        organization = organization_element.text.strip()

        # Find the job description element
        job_description_element = soup.find(
            "div", {"class": "show-more-less-html__markup"}
        )

        # Extract the job description and concatenate its elements
        job_description = ""
        if job_description_element:
            for element in job_description_element.contents:
                job_description += str(element.text+"\n")

        # Return the job details
        return self.generate_json((job_title, organization, job_description))

    def generate_json(self, job_details):

        self.__extractor = DataExtractor(job_details[2])
        job_json = {
            "job_title": job_details[0],
            "organization": job_details[1],
            "job_description": job_details[2],
            "frequency_of_keywords": self.__extractor.frequency_of_keywords(),
        }
        return job_json
