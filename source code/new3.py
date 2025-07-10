import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch Chrome with undetected_chromedriver
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

# Open Glassdoor review page
driver.get("https://www.glassdoor.co.in/Reviews/Oracle-Reviews-E1737.htm")

# Let the page load completely
time.sleep(10)

# Initialize a list to store review data
reviews_data = []
collected_reviews = 0
max_reviews = 100


def format_and_print_review(review, review_number):
    """Format and print a review in the desired output format."""
    print("-" * 50)
    print(f"Review {review_number}:")
    for key, value in review.items():
        print(f" {key}: {value}")
    print("-" * 50)


def detect_icon_status(container_div):
    """
    Detects if an icon block represents 'Yes' (tick present) or 'No' (empty circle or cross).
    """
    if not container_div:
        return "No"  # Default to "No" if the container is not found

    svg = container_div.find("svg")
    if svg:
        # Check for a path element
        path = svg.find("path")
        if path:
            path_data = path.get("d", "")

            # Tick check (✔️ pattern)
            if "8.835" in path_data or "17.64" in path_data:
                return "Yes"

    return "No"


def parse_reviews():
    """Parse reviews from the current page."""
    global collected_reviews
    try:
        # Retry mechanism for loading review blocks
        for attempt in range(3):  # Retry up to 3 times
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-test='review-details-container']"))
                )
                break  # Exit retry loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 2:  # Retry if attempts remain
                    driver.refresh()
                    time.sleep(5)  # Wait for the page to reload
                else:
                    raise  # Raise the exception after final attempt

    except Exception as e:
        print(f"Error waiting for review blocks: {e}")
        # Save the page source for debugging
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return False

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    review_blocks = soup.find_all("div", {"data-test": "review-details-container"})

    if not review_blocks:
        print("No review blocks found on this page.")
        return False

    for review_block in review_blocks:
        if collected_reviews >= max_reviews:
            return False

        # Extract review details
        result = {}
        rating_divs = review_block.find_all("div", class_="rating-icon_ratingContainer__9UoJ6")

        for div in rating_divs:
            label = div.find("span").text.strip()
            path_tag = div.find("path")

            if path_tag:
                d_attr = path_tag.get("d", "")
                if "8.835" in d_attr:  # Tick
                    result[label] = "Yes"
                elif "18.299" in d_attr:  # Cross
                    result[label] = "No"
                else:
                    result[label] = "Unknown"
            else:
                result[label] = "No"

        review = {
            "Company": "Oracle",  # Add the company column
            "Rating": review_block.select_one("span[data-test='review-rating-label']").get_text(strip=True) if review_block.select_one("span[data-test='review-rating-label']") else "N/A",
            "Date": review_block.select_one("span.timestamp_reviewDate__dsF9n").get_text(strip=True) if review_block.select_one("span.timestamp_reviewDate__dsF9n") else "N/A",
            "Title": review_block.select_one("h3[data-test='review-details-title']").get_text(strip=True) if review_block.select_one("h3[data-test='review-details-title']") else "N/A",
            "Role": review_block.select_one("span[data-test='review-avatar-label']").get_text(strip=True) if review_block.select_one("span[data-test='review-avatar-label']") else "N/A",
            "Location": review_block.find("div", class_="text-with-icon_LabelContainer__xbtB8").get_text(strip=True) if review_block.find("div", class_="text-with-icon_LabelContainer__xbtB8") else "N/A",
            "Pros": review_block.find("span", {"data-test": "review-text-PROS"}).get_text(strip=True) if review_block.find("span", {"data-test": "review-text-PROS"}) else "N/A",
            "Cons": review_block.find("span", {"data-test": "review-text-CONS"}).get_text(strip=True) if review_block.find("span", {"data-test": "review-text-CONS"}) else "N/A",
            "Recommend": result.get("Recommend", "Unknown"),
            "CEO Approval": result.get("CEO approval", "Unknown"),
            "Business Outlook": result.get("Business outlook", "Unknown"),
        }

        reviews_data.append(review)
        collected_reviews += 1

        # Format and print the review
        format_and_print_review(review, collected_reviews)

    return True


def navigate_to_next_page():
    """Navigate to the next page in the pagination."""
    try:
        # Wait for the pagination container to load
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='next-page']"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
        next_button.click()
        time.sleep(5)  # Wait for the next page to load
        return True
    except Exception as e:
        print(f"Error navigating to the next page: {e}")
        return False


# Main loop to parse reviews and navigate through pages
try:
    while collected_reviews < max_reviews:
        if not parse_reviews():
            print("Stopping review collection as no reviews were found on this page.")
            break
        if not navigate_to_next_page():
            print("Stopping review collection as navigation to the next page failed.")
            break
finally:
    # Ensure the browser is closed properly
    try:
        driver.quit()
    except Exception as e:
        print(f"Error during driver quit: {e}")

# Save the reviews data to an Excel file
if reviews_data:
    try:
        df = pd.DataFrame(reviews_data)
        output_file = "oracle_reviews.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Reviews saved to {output_file}")
    except PermissionError:
        print(f"Permission denied: Unable to save {output_file}. Please close the file if it is open and try again.")
    except Exception as e:
        print(f"Error saving to Excel: {e}")