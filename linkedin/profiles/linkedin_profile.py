import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def login_to_linkedin(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Add this line to run headless
    driver = webdriver.Chrome(options=options)
    driver.get("https://linkedin.com/uas/login")
    time.sleep(5)
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    return driver

def scroll_page(driver, duration=20):
    start = time.time()
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        end = time.time()
        if round(end - start) > duration:
            break

def extract_profile_info(driver, profile_url):
    driver.get(profile_url)
    time.sleep(5)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
    name_loc = intro.find("h1")
    name = name_loc.get_text().strip()
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    works_at = works_at_loc.get_text().strip()
    location_loc = intro.find_all("span", {'class': 'text-body-small'})
    location = location_loc[0].get_text().strip()
    return name, works_at, location

def extract_experience_info(driver):
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    experience = soup.find("section", {"id": "experience-section"}).find('ul')
    li_tags = experience.find('div')
    a_tags = li_tags.find("a")
    job_title = a_tags.find("h3").get_text().strip()
    company_name = a_tags.find_all("p")[1].get_text().strip()
    joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()
    employment_duration = a_tags.find_all("h4")[1].find_all("span")[1].get_text().strip()
    return job_title, company_name, joining_date, employment_duration

def extract_job_info(driver):
    jobs = driver.find_element(By.XPATH, "//a[@data-link-to='jobs']/span")
    jobs.click()
    job_src = driver.page_source
    soup = BeautifulSoup(job_src, 'lxml')
    jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
    job_titles = [title.text.strip() for title in jobs_html]
    company_name_html = soup.find_all('div', {'class': 'job-card-container__company-name'})
    company_names = [name.text.strip() for name in company_name_html]
    location_html = soup.find_all('ul', {'class': 'job-card-container__metadata-wrapper'})
    location_list = [re.sub('\n\n +', ' ', loc.text.strip()) for loc in location_html]
    return job_titles, company_names, location_list

def main():
    # Define login credentials
    username = 'your_username'
    password = 'your_password'
    profile_url = "https://www.linkedin.com/in/kunalshah1/"
    
    # Login to LinkedIn
    driver = login_to_linkedin(username, password)
    
    # Extract profile information
    name, works_at, location = extract_profile_info(driver, profile_url)
    print("Name -->", name, "\nWorks At -->", works_at, "\nLocation -->", location)
    
    # Scroll page
    scroll_page(driver)
    
    # Extract experience information
    job_title, company_name, joining_date, employment_duration = extract_experience_info(driver)
    print("Job Title -->", job_title, "\nCompany Name -->", company_name, "\nJoining Date -->", joining_date, "\nEmployment Duration -->", employment_duration)
    
    # Extract job information
    job_titles, company_names, location_list = extract_job_info(driver)
    print("Job Titles -->", job_titles, "\nCompany Names -->", company_names, "\nLocations -->", location_list)
    
    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()





