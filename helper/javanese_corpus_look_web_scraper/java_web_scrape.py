from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

# === SETUP ===
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # comment out this line if you want to see the browser
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("media.volume_scale", "0.0")

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 15)

BASE_URL = "https://www.sastra.org/koleksi"
driver.get(BASE_URL)
os.makedirs("sastra_output", exist_ok=True)

page = 1
total_scraped = 0

while True:
    print(f"\n📄 Now scraping page {page}...")

    # Wait until the table containing the article list appears
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ysl-ovf-aux div.ysl-tbl")))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select("div.ysl-ovf-aux div.ysl-tbl tbody tr")

    if not rows:
        print("⚠️ No rows found on this page.")
        break

    print(f"🔗 Found {len(rows)} articles on page {page}")

    for i, row in enumerate(rows, start=1):
        link_tag = row.find("a", href=True)
        if not link_tag:
            continue

        href = link_tag["href"]
        full_url = "https://www.sastra.org" + href

        # Open article page
        driver.get(full_url)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.com-content-article__body div#mark_range")))
            article_soup = BeautifulSoup(driver.page_source, "html.parser")
            content_div = article_soup.select_one("div.com-content-article__body div#mark_range")

            if content_div:
                text = content_div.get_text(separator="\n", strip=True)
                filename = f"sastra_output/page{page:03d}_entry{i:03d}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                total_scraped += 1
                print(f"📝 Scraped ({total_scraped}): {href}")

        except Exception as e:
            print(f"⚠️ Error scraping {href}: {e}")

        # Go back to the main article list
        driver.back()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ysl-ovf-aux div.ysl-tbl")))
        time.sleep(1.5)

    # Try to click the "Maju satu halaman" button
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[title="Maju satu halaman"]')
        if "disabled" in next_button.get_attribute("class"):
            print("🚫 Next button disabled. End of list.")
            break
        next_button.click()
        time.sleep(3)
        page += 1
    except Exception:
        print("🚫 No next button found. Stopping.")
        break

driver.quit()
print(f"\n✅ Done! Scraped {total_scraped} total articles.")
