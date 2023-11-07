import csv
import os
import urllib
from random import shuffle
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from Bot import Bot
import re
import datetime
import sys

class StackScraper(Bot):
    def __init__(self):
        super().__init__(verbose=True)

        role_names = [
            "Machine Learning Engineer", 
            "Data Engineer",
            "Data Analyst",
            "Data Scientist"
        ]

        self.driver.get("https://www.google.com")
        for role_name in role_names:
            self.get_all_jobs(role_name)
        
    def get_all_jobs(self, role_name):
        query = f"https://www.google.com/search?q={role_name} jobs&ibp=htl;jobs#htivrt=jobs".replace(' ', '+')
        print(query)
        self.driver.get(query)
        listings = self.driver.find_elements(By.XPATH, "//div[@class='PwjeAc']")
        print("Number of listings:", len(listings))

        sleep(1)

        for idx, listing in enumerate(listings):
            self.scroll_into_view(listing)
            listing.click()
            sleep(0.5)
            try:
                job = self._get_job()
            except:
                continue
            self.save_job(job, role_name)
        
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
    def _get_job(self):

        results = self._get_company()

        job_id = self._get_job_id()
        print("Job ID:", job_id)
        company = results[0]
        print("Company:", company)
        description = self._get_job_description()
        remote = results[1]
        print("Remoto", remote)
        return {
            "id": job_id,
            "company": company,
            "description": description,
            "Remote": remote
        }

    def _get_job_id(self):
        parsed_url = urllib.parse.urlparse(self.driver.current_url)
        id = urllib.parse.parse_qs(parsed_url.fragment)['htidocid'][0]
        return id
    
    def _get_company(self):
        job_containers = self.driver.find_elements(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
        companies = []
        remote_statuses = []
        for job_container in job_containers:
            company = job_container.find_element(
                By.XPATH, './/div[@class="nJlQNd sMzDkb"]').text.strip("[]")
            remote_status = job_container.find_element(
                By.XPATH, './/div[@class="sMzDkb"]').text.strip("[]")
            companies.append(company)
            remote_statuses.append(remote_status)
          # Concatenate the company names into a single string
        companies_string = ", ".join(companies)
        remote_string = ", ".join(remote_statuses)
        return companies_string, remote_string  
    
    #def _get_remote(self):
        job_containers = self.driver.find_elements(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
        remote_statuses = []
        for job_container in job_containers:
            remote_status = job_container.find_element(
                By.XPATH, './/div[@class="sMzDkb"]').text.strip("[]")
            remote_statuses.append(remote_status)
        return remote_statuses



# ...

    def _get_job_description(self):
        job_containers = self.driver.find_elements(
            By.XPATH, '//div[@class="whazf bD1FPe"]')
        descriptions = []
        for job_container in job_containers:
            try:
                expand_description_button = job_container.find_element(
                    By.XPATH, ".//div/div/div/div/div/div/div[@class='CdXzFe j4kHIf']")
                self.scroll_into_view(expand_description_button)
                expand_description_button.click()
            except NoSuchElementException:
                pass
            description_element = job_container.find_element(
                By.XPATH, ".//span[@class='HBvzbc']")
            description = description_element.text
            # Remove newline characters and HTML tags
            cleaned_description = re.sub(r'\n|<.*?>', ' ', description)
            descriptions.append(cleaned_description)
            # Concatenate the descriptions into a single string
            descriptions_string = " ".join(descriptions)
            return descriptions_string


    
    def save_job(self, job, role_name):
        try:
            output_name = sys.argv[1]
        except Exception as e:
                 print(f"Error with file input. Error {e}")
                 sys.exit(1)
        


        if self.verbose: 
            print(f'Saving {role_name} job')

        folder_path = "raw_data"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{output_name}.csv")
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Job_ID", "Job_Role", "Job_Company", "Job_Description", "URL", "Date", "Remote"])

        with open(file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            url = self.driver.current_url
            timestamp_date = datetime.datetime.now().strftime("%Y-%m-%d")
            writer.writerow([job["id"], role_name, job["company"], job["description"],url, timestamp_date, job["Remote"] ])
        
        print("CSV file created.")


if __name__ == '__main__':
    StackScraper()
    
 