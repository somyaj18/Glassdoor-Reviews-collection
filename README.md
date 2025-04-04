# Glassdoor-Reviews-collection
Glassdoor Review Scraper 🏢🔍
This project is an automated web scraper that extracts employee reviews from Glassdoor using Selenium, BeautifulSoup, and Pandas. The extracted data includes company name, ratings, pros, cons, employee status, location, and more. The results are saved in an Excel file for further analysis.

## Features ✨
✅ Automated Glassdoor Review Extraction – Fetches reviews, ratings, and company details
✅ Bypasses Bot Detection – Uses undetected_chromedriver to avoid detection
✅ Dynamic Scrolling – Loads more reviews automatically
✅ Structured Data Extraction – Collects position, location, employee status, and key sentiments
✅ Saves to Excel – Stores the extracted data in a structured format


### Requirements 📦
Python 3.x

Selenium

BeautifulSoup

Pandas

undetected_chromedriver

### Install dependencies using:

pip install undetected-chromedriver pandas beautifulsoup4 selenium openpyxl
### How It Works ⚡
1️⃣ Opens Glassdoor review page for a company
2️⃣ Scrolls down to load more reviews
3️⃣ Extracts key information such as:

Company Name

Overall Rating

Pros & Cons

Employee Position & Status

Location

Review Page URL
4️⃣ Saves the data in an Excel file (glassdoor_reviews.xlsx)

### Example Output (Excel Format) 📊
Company Name	Date	Review Page	Position	Location	Employee Status	Overall Rating	Pros	Cons
Google	2025-04-04	link_here	Engineer	California	Former Employee	4.5	Great culture	Long hours
License 📝
