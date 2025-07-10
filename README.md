# 🚀 Glassdoor Oracle Reviews Scraper

This is a **Python web scraping project** that uses **Selenium**, **BeautifulSoup**, and **Pandas** to extract reviews of **Oracle** from Glassdoor.  
It captures the review title, rating, date, employee role, location, pros, cons, and indicators like whether they recommend the company, approve the CEO, and business outlook.  
Finally, it saves everything into an **Excel file**.

---

## 💻 Tech Stack
- **Python**
- **Selenium (undetected-chromedriver)** – to automate Chrome and bypass anti-bot detection
- **BeautifulSoup** – for parsing loaded HTML
- **Pandas** – to save data into Excel

---

## 📦 Installation, Setup & Run (all together)
✅ Clone this repository, install the packages, and run the script — all in one go:

```bash
git clone https://github.com/your-username/glassdoor-oracle-reviews-scraper.git
cd glassdoor-oracle-reviews-scraper
pip install selenium undetected-chromedriver beautifulsoup4 pandas openpyxl
python new3.py


## 🚀 Example Output In Terminal


--------------------------------------------------
Review 1:
 Company: Oracle
 Rating: 4.0
 Date: Mar 10, 2025
 Title: Great place to work
 Role: Senior Developer
 Location: Bengaluru, India
 Pros: Work-life balance is good
 Cons: Slow growth
 Recommend: Yes
 CEO Approval: Yes
 Business Outlook: No
--------------------------------------------------
...
Reviews saved to oracle_reviews.xlsx


