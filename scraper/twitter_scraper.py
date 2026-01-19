from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta, timezone
import time
import random


class TwitterScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()

        options.add_argument(
            r"--user-data-dir=C:\Users\kribisht\AppData\Local\Google\Chrome\SeleniumProfile"
        )

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=options)

        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            },
        )

    def scrape_hashtag(
        self,
        hashtag,
        max_tweets=500,
        max_scrolls=40,
        max_idle_scrolls=5
    ):
        url = f"https://twitter.com/search?q=%23{hashtag}&f=live"
        self.driver.get(url)
        time.sleep(15)
        WebDriverWait(self.driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        self._human_delay(4, 6)

        tweets_seen = set()
        results = []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=48)

        scroll_count = 0
        idle_scrolls = 0

        while True:
            # 🚨 Detect broken page early
            if self._page_broken():
                print("Page broken — cooling down")
                self._human_delay(30, 60)
                self.driver.refresh()
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "article"))
                )
                self._human_delay(4, 6)

            cards = self.driver.find_elements(By.XPATH, "//article")
            new_in_this_scroll = 0

            for card in cards:
                try:
                    text_el = card.find_element(By.XPATH, ".//div[@lang]")
                    text = text_el.text.strip()

                    if not text or text in tweets_seen:
                        continue

                    time_el = card.find_element(By.XPATH, ".//time")
                    tweet_time = datetime.fromisoformat(
                        time_el.get_attribute("datetime").replace("Z", "+00:00")
                    )

                    if tweet_time < cutoff_time:
                        return results

                    tweets_seen.add(text)
                    new_in_this_scroll += 1

                    results.append({
                        "hashtag": hashtag,
                        "content": text,
                        "timestamp": tweet_time
                    })

                    if len(results) >= max_tweets:
                        return results

                except:
                    continue

            if new_in_this_scroll == 0:
                idle_scrolls += 1
            else:
                idle_scrolls = 0

            if idle_scrolls >= max_idle_scrolls:
                return results

            if scroll_count >= max_scrolls:
                return results

            scroll_count += 1
            self._scroll()

    def _scroll(self):
        for _ in range(random.randint(2, 4)):
            self.driver.execute_script("window.scrollBy(0, 350)")
            self._human_delay(1.2, 2.2)

    def _page_broken(self):
        return "Something went wrong" in self.driver.page_source

    def _human_delay(self, a=2, b=4):
        time.sleep(random.uniform(a, b))

    def close(self):
        self.driver.quit()
