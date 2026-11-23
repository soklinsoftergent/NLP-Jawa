from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- SETUP ---
driver = webdriver.Firefox()
driver.get("https://www.sastra.org/koleksi")
wait = WebDriverWait(driver, 10)

page_num = 1

while True:
    print(f"📄 Now scraping page {page_num}...")

    # Wait for article list table to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ysl-ovf-aux tbody")))

    parent = driver.find_element(By.CSS_SELECTOR, "div.ysl-ovf-aux tbody")
    rows = parent.find_elements(By.CSS_SELECTOR, "tr td a")

    for i in range(len(rows)):
        rows = driver.find_elements(By.CSS_SELECTOR, "div.ysl-ovf-aux tbody tr td a")
        link = rows[i]
        title = link.text.strip()
        print(f"  → Scraping: {title}")
        link.click()

        try:
            # Wait for article content to appear
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.com-content-article__body div#mark_range")
            ))
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "div#mark_range p")

            if paragraphs:
                text = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
                with open("scrapped_java.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n\n===== {title} =====\n")
                    f.write(text)
                    f.write("\n")
            else:
                print(f"  ⚠️ No <p> text found for: {title}")

        except Exception as e:
            print(f"  ⚠️ Skipped '{title}' — error or timeout: {e.__class__.__name__}")

        driver.back()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ysl-ovf-aux tbody")))

    # Try to move to the next page
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'button[title="Maju satu halaman"]')
        if next_button.get_attribute("disabled"):
            print("✅ No more pages. Done.")
            break
        next_button.click()
        page_num += 1
        time.sleep(2)
    except Exception as e:
        print("⚠️ Next page button not found or failed:", e)
        break

driver.quit()
