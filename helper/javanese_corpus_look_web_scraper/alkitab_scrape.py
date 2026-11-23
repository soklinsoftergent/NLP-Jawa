from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get(r"https://alkitab.me/jv-jawa/Purwaning%20Dumadi/")
driver.implicitly_wait(0.5)

while True:
    main = driver.find_element(By.ID, "the-content")
    with open(r"javanese corpus.txt/alkitab_jawa.txt", "a", encoding="utf-8") as f:
        f.write(main.text)

    next = driver.find_element(By.CSS_SELECTOR, ".next-chapter.pull-right")
    try:
        next.click()
    except:
        print("Couldn't find element, breaking...")
        break

driver.quit()


