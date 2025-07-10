import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Launch Undetected Chrome
driver = uc.Chrome(headless=False)  # headless=True to hide browser
driver.get("https://www.glassdoor.co.in/Reviews/Oracle-Reviews-E1737.htm")

# Wait for page to load
time.sleep(20)

# Print Page Title
print("Page Title:", driver.title)

# Close driver
driver.quit()

