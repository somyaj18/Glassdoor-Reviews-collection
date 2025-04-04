import undetected_chromedriver as uc
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--ignore-certificate-errors")

#  Initialize WebDriver
driver = uc.Chrome(headless=False)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#  Open Glassdoor and Load More Reviews
url = "https://www.glassdoor.com/Reviews/Google-Reviews-E9079.htm"
driver.get(url)
time.sleep(5)

for _ in range(3):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

#Step 3: Parse Page Source
soup = BeautifulSoup(driver.page_source, "html.parser")
try:
#  Extract Company Name
    try:
        company_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.employer-header_employerHeader__LPAMn"))
        ).text.strip()
    except:
        company_name = "Not Found"

# Extract Review Page Link
    def review_link():
        try:
            link_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@data-test='ei-nav-reviews-link']"))
            )
            return link_tag.get_attribute("href")
        except:
            return "Not Found"
    # Extract Overall Rating
    def overall_rating():
        try:
            rating_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ratingNumber')]"))
            )
            return rating_span.text.strip()
        except:
            return "Not Found"

    # Extract Pros
    def pros():
        try:
            pros_div = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='pros']"))
            )
            return pros_div[0].text.strip() if pros_div else "Not Found"
        except:
            return "Not Found"

    # Extract Cons
    def cons():
        try:
            cons_div = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='cons']"))
            )
            return cons_div[0].text.strip() if cons_div else "Not Found"
        except:
            return "Not Found"

    # Extract Location
    def location():
        try:
            loc_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test='location']"))
            )
            return loc_div.text.strip()
        except:
            return "Not Found"

    # Extract Position
    def position():
        try:
            pos_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test='position']"))
            )
            return pos_span.text.strip()
        except:
            return "Not Found"

    # Extract Employee Status
    def employee_status():
        try:
            emp_span = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-test='employee-status']"))
            )
            return emp_span.text.strip()
        except:
            return "Not Found"

    # Extract Current Date
    def today_date():
        return date.today()

    # Data for Pandas DataFrame
    data = {
        "Company Name": [company_name],
        "Date": [today_date()],
        "Review Page": [review_link()],
        "Position": [position()],
        "Location": [location()],
        "Employee Status": [employee_status()],
        "Overall Rating": [overall_rating()],
        "Pros": [pros()],
        "Cons": [cons()],
        "Recommend": ["YES"],
        "Business Outlook": ["YES"],
        "CEO Approval": ["YES"],
        "Work/Life balance": [5],
        "Culture and values": [5],
        "Diversity and inclusion": [5],
        "Career opportunities": [5],
        "Compensation and benefits": [5],
        "Senior management": [5]
    }

    df = pd.DataFrame(data)


    df.to_excel("glassdoor_reviews.xlsx", index=False)
finally:
    if driver:
        driver.quit()
print(" Data Scraped & Saved Successfully!")
