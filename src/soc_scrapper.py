import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -----------------------
# Chrome Options
# -----------------------
options = webdriver.ChromeOptions()
# Run non-headless
# options.add_argument("--headless")  # COMMENT OUT to reduce CAPTCHA
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# -----------------------
# Google Jobs Search URL
# -----------------------
SEARCH_QUERY = "SOC ANALYST TIER 1"
url = f"https://www.google.com/search?q={SEARCH_QUERY.replace(' ','+')}&ibp=htl;jobs"
driver.get(url)

wait = WebDriverWait(driver, 20)
job_data = []

# -----------------------
# Switch into jobs iframe
# -----------------------
try:
    iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[id^='goog_jobs']")))
    driver.switch_to.frame(iframe)
except:
    print("Could not find jobs iframe. CAPTCHA might have triggered or page changed.")
    driver.quit()
    exit()

# -----------------------
# Wait for job cards
# -----------------------
try:
    job_cards = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul[role='list'] li"))
    )
    print(f"Found {len(job_cards)} job cards")
except:
    print("Could not find job cards. CAPTCHA might have triggered.")
    driver.quit()
    exit()

# -----------------------
# Scrape each job card
# -----------------------
for idx, card in enumerate(job_cards):
    try:
        # scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", card)
        time.sleep(random.uniform(1.5, 3.0))  # human-like delay
        card.click()
        time.sleep(random.uniform(2.0, 4.0))  # wait for popup to load

        # Job Title
        job_title = driver.find_element(By.CSS_SELECTOR, "h2").text

        # Full description container
        desc_container = driver.find_element(By.CSS_SELECTOR, "#job_details_container")
        desc_text = desc_container.text

        # Extract Responsibilities section
        resp_text = ""
        if "responsibilities" in desc_text.lower():
            resp_text = desc_text.split("Responsibilities",1)[1]
            for stop_word in ["Qualifications","Requirements","Description"]:
                if stop_word in resp_text:
                    resp_text = resp_text.split(stop_word,1)[0]
                    break
            resp_text = resp_text.strip()

        job_data.append({
            "Job Title": job_title,
            "Responsibilities": resp_text if resp_text else "Not found"
        })
        print(f"[{idx+1}] Scraped: {job_title}")

        # small random delay between jobs
        time.sleep(random.uniform(1.5, 3.0))

    except Exception as e:
        print(f"Failed on job {idx}: {e}")
        continue

# -----------------------
# Save results
# -----------------------
df = pd.DataFrame(job_data)
df.to_csv("google_jobs_hardened.csv", index=False, encoding="utf-8")
driver.quit()
print("✅ Scraping finished! Data saved to google_jobs_hardened.csv")
