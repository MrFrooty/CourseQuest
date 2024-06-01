# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# def scrape_linkedin_profile(linkedin_url, email, password):
    # options = Options()
    # options.headless = True  # Run in headless mode
    # driver = webdriver.Chrome(
    #     service=Service("/Users/freddy/Downloads/chromedriver-mac-arm64/chromedriver"),
    #     options=options,
    # )

#     try:
#         # Navigate to LinkedIn login page
#         driver.get("https://www.linkedin.com/login")

#         # Log in
#         email_input = driver.find_element(By.ID, "vizjob0531@gmail.com")
#         email_input.send_keys(email)
#         password_input = driver.find_element(By.ID, "Vizjob!=0531$")
#         password_input.send_keys(password)
#         password_input.send_keys(Keys.RETURN)

#         # Wait for login to complete
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".global-nav__me"))
#         )

#         # Navigate to the profile page
#         driver.get(linkedin_url)

#         # Wait for the profile page to load
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".pv-top-card"))
#         )

#         # Get the page source and parse it with BeautifulSoup
#         html_content = driver.page_source
#         soup = BeautifulSoup(html_content, "html.parser")

#         # Extract experience section
#         experiences = []
#         experience_section = soup.find("section", {"id": "experience-section"})
#         if experience_section:
#             for experience in experience_section.find_all(
#                 "li", class_="pv-entity__position-group-pager"
#             ):
#                 title = (
#                     experience.find("h3").get_text(strip=True)
#                     if experience.find("h3")
#                     else None
#                 )
#                 company = (
#                     experience.find("p", class_="pv-entity__secondary-title").get_text(
#                         strip=True
#                     )
#                     if experience.find("p", class_="pv-entity__secondary-title")
#                     else None
#                 )
#                 date_range = (
#                     experience.find("h4", class_="pv-entity__date-range").get_text(
#                         strip=True
#                     )
#                     if experience.find("h4", class_="pv-entity__date-range")
#                     else None
#                 )
#                 experiences.append(
#                     {"title": title, "company": company, "date_range": date_range}
#                 )

#         # Extract projects section
#         projects = []
#         projects_section = soup.find("section", {"id": "projects-section"})
#         if projects_section:
#             for project in projects_section.find_all(
#                 "li", class_="pv-entity__position-group-pager"
#             ):
#                 project_name = (
#                     project.find("h3").get_text(strip=True)
#                     if project.find("h3")
#                     else None
#                 )
#                 project_description = (
#                     project.find("p", class_="pv-entity__description").get_text(
#                         strip=True
#                     )
#                     if project.find("p", class_="pv-entity__description")
#                     else None
#                 )
#                 projects.append(
#                     {
#                         "project_name": project_name,
#                         "project_description": project_description,
#                     }
#                 )

#         # Extract skills section
#         skills = []
#         skills_section = soup.find("section", {"id": "skills-section"})
#         if skills_section:
#             for skill in skills_section.find_all(
#                 "span", class_="pv-skill-category-entity__name-text"
#             ):
#                 skills.append(skill.get_text(strip=True))

#         # Extract organizations section
#         organizations = []
#         organizations_section = soup.find("section", {"id": "organizations-section"})
#         if organizations_section:
#             for organization in organizations_section.find_all(
#                 "li", class_="pv-entity__position-group-pager"
#             ):
#                 organization_name = (
#                     organization.find("h3").get_text(strip=True)
#                     if organization.find("h3")
#                     else None
#                 )
#                 organization_role = (
#                     organization.find(
#                         "p", class_="pv-entity__secondary-title"
#                     ).get_text(strip=True)
#                     if organization.find("p", class_="pv-entity__secondary-title")
#                     else None
#                 )
#                 organizations.append(
#                     {
#                         "organization_name": organization_name,
#                         "organization_role": organization_role,
#                     }
#                 )

#         return {
#             "experiences": experiences,
#             "projects": projects,
#             "skills": skills,
#             "organizations": organizations,
#         }

#     finally:
#         driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

options = Options()
options.headless = False
    
driver = webdriver.Chrome(
        service=Service("/Users/freddy/Downloads/chromedriver-mac-arm64/chromedriver"),
        options=options,
    )


# Login
def login(email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    eml = driver.find_element(by=By.ID, value="username")
    eml.send_keys(email)
    passwd = driver.find_element(by=By.ID, value="password")
    passwd.send_keys(password)
    loginbutton = driver.find_element(
        by=By.XPATH, value='//*[@id="organic-div"]/form/div[3]/button'
    )
    loginbutton.click()
    time.sleep(3)


# Return all profiles urls of M&A employees of a certain company
def getProfileURLs(companyName):
    time.sleep(1)
    driver.get(
        "https://www.linkedin.com/company/"
        + companyName
        + "/people/?keywords=M%26A%2CMergers%2CAcquisitions"
    )
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    source = BeautifulSoup(driver.page_source)

    visibleEmployeesList = []
    visibleEmployees = source.find_all("a", class_="app-aware-link")
    for profile in visibleEmployees:
        if profile.get("href").split("/")[3] == "in":
            visibleEmployeesList.append(profile.get("href"))

    invisibleEmployeeList = []
    invisibleEmployees = source.find_all(
        "div",
        class_="artdeco-entity-lockup artdeco-entity-lockup--stacked-center artdeco-entity-lockup--size-7 ember-view",
    )
    for invisibleguy in invisibleEmployees:
        title = (
            invisibleguy.findNext(
                "div", class_="lt-line-clamp lt-line-clamp--multi-line ember-view"
            )
            .contents[0]
            .strip("\n")
            .strip("  ")
        )
        invisibleEmployeeList.append(title)

        # A profile can either be visible or invisible
        profilepiclink = ""
        visibleProfilepiclink = invisibleguy.find("img", class_="lazy-image ember-view")
        invisibleProfilepicLink = invisibleguy.find(
            "img", class_="lazy-image ghost-person ember-view"
        )
        if visibleProfilepiclink == None:
            profilepiclink = invisibleProfilepicLink.get("src")
        else:
            profilepiclink = visibleProfilepiclink.get("src")

        if profilepiclink not in invisibleEmployees:
            invisibleEmployeeList.append(profilepiclink)
    return (visibleEmployeesList[5:], invisibleEmployeeList)


# Testing spreadsheet of urls
# profilesToSearch = pd.DataFrame(columns=["ProfileID", "Title", "ProfilePicLink"])
# company = 'apple'
# searchable = getProfileURLs(company)
#
# for profileId in searchable[0]:
#     profilesToSearch.loc[len(profilesToSearch.index)] = [profileId, "", ""]
# for i in range(0, len(searchable[1]), 2):
#     profilesToSearch.loc[len(profilesToSearch.index)] = ["", searchable[1][i], searchable[1][i+1]]


# parses a type 2 job row
def parseType2Jobs(alltext):
    jobgroups = []
    company = alltext[16][: len(alltext[16]) // 2]
    totalDurationAtCompany = alltext[20][: len(alltext[20]) // 2]

    # get rest of the jobs in the same nested list
    groups = []
    count = 0
    index = 0
    for a in alltext:
        if a == "" or a == " ":
            count += 1
        else:
            groups.append((count, index))
            count = 0
        index += 1

    numJobsInJoblist = [
        g for g in groups if g[0] == 21 or g[0] == 22 or g[0] == 25 or g[0] == 26
    ]
    for i in numJobsInJoblist:
        # full time/part time case
        if "time" in alltext[i[1] + 5][: len(alltext[i[1] + 5]) // 2].lower().split(
            "-"
        ):
            jobgroups.append(
                (
                    alltext[i[1]][: len(alltext[i[1]]) // 2],
                    alltext[i[1] + 8][: len(alltext[i[1] + 8]) // 2],
                )
            )
        else:
            jobgroups.append(
                (
                    alltext[i[1]][: len(alltext[i[1]]) // 2],
                    alltext[i[1] + 4][: len(alltext[i[1] + 4]) // 2],
                )
            )
    return ("type2job", company, totalDurationAtCompany, jobgroups)


# parses a type 1 job row
def parseType1Job(alltext):
    jobtitle = alltext[16][: len(alltext[16]) // 2]
    company = alltext[20][: len(alltext[20]) // 2]
    duration = alltext[23][: len(alltext[23]) // 2]
    return ("type1job", jobtitle, company, duration)


# returns linkedin profile information
def scrape_linkedin_profile(employeeLink, companyName):
    url = employeeLink
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")

    profile = []
    profile.append(companyName)
    info = source.find("div", class_="mt2 relative")
    name = (
        info.find(
            "h1", class_="text-heading-xlarge inline t-24 v-align-middle break-words"
        )
        .get_text()
        .strip()
    )
    title = (
        info.find("div", class_="text-body-medium break-words")
        .get_text()
        .lstrip()
        .strip()
    )
    profile.append(name)
    profile.append(title)
    time.sleep(1)
    experiences = source.find_all(
        "li",
        class_="artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column",
    )

    for x in experiences[1:]:
        alltext = x.getText().split("\n")
        print(alltext)
        startIdentifier = 0
        for e in alltext:
            if e == "" or e == " ":
                startIdentifier += 1
            else:
                break
        # jobs, educations, certifications
        if startIdentifier == 16:
            # education
            if (
                "university" in alltext[16].lower().split(" ")
                or "college" in alltext[16].lower().split(" ")
                or "ba" in alltext[16].lower().split(" ")
                or "bs" in alltext[16].lower().split(" ")
            ):
                profile.append(
                    (
                        "education",
                        alltext[16][: len(alltext[16]) // 2],
                        alltext[20][: len(alltext[20]) // 2],
                    )
                )

            # certifications
            elif "issued" in alltext[23].lower().split(" "):
                profile.append(
                    (
                        "certification",
                        alltext[16][: len(alltext[16]) // 2],
                        alltext[20][: len(alltext[20]) // 2],
                    )
                )

        elif startIdentifier == 12:
            # Skills
            if (alltext[16] == "" or alltext[16] == " ") and len(alltext) > 24:
                profile.append(("skill", alltext[12][: len(alltext[12]) // 2]))

    # experiences
    url = driver.current_url + "/details/experience/"
    driver.get(url)
    time.sleep(2)
    source = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(1)
    exp = source.find_all("li")
    for e in exp[13:]:
        row = e.getText().split("\n")
        if row[:16] == [
            "",
            "",
            "",
            "",
            "",
            "",
            " ",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]:
            if "yrs" in row[20].split(" "):
                profile.append(parseType2Jobs(row))
            else:
                profile.append(parseType1Job(row))

    return profile


if __name__ == "__main__":
    login("vizjob0531@gmail.com", "Vizjob!=0531$")
    employees = {}
    company = "apple"
    searchable = getProfileURLs(company)
    for employee in searchable:
        employees[employee] = scrape_linkedin_profile(employee, company)
    with open("m&a.json", "w") as f:
        json.dump(employees, f)
    time.sleep(10)
    driver.quit()
