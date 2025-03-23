# import requests
# import logging
# import random
# import time
# import threading
# import undetected_chromedriver as uc

# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from flask_socketio import SocketIO
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# class SiteMonitor:
#     def __init__(self, socketio: SocketIO):
#         self.socketio = socketio
#         self.sites = {}
#         self.lock = threading.Lock()

#         # ✅ Advanced User-Agent Pool
#         self.user_agents = [
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#             "Mozilla/5.0 (Linux; Android 11; SM-G988U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
#             "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
#         ]

#     def check_site_status(self, url):
#         """Quickly check site status using requests, then use Selenium if blocked."""
#         headers = {"User-Agent": random.choice(self.user_agents)}

#         try:
#             response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
#             status_code = response.status_code

#             logging.info(f"Checked {url} - Status Code: {status_code}")

#             if status_code == 403:
#                 logging.warning(f"Bot detected! Switching to Selenium for {url}")
#                 return self._selenium_check(url)

#             if 200 <= status_code < 400:
#                 return self._create_status(url, "UP", status_code)

#             return self._create_status(url, "DOWN", status_code)

#         except requests.exceptions.RequestException as e:
#             logging.error(f"Request failed for {url}: {e}")
#             return self._selenium_check(url)

#     def _selenium_check(self, url):
#         """Use undetected Selenium with advanced evasion techniques."""
#         try:
#             options = uc.ChromeOptions()
#             options.add_argument("--headless=new")  # For Chrome 109+
#             options.add_argument("--disable-gpu")
#             options.add_argument("--no-sandbox")
#             options.add_argument("--disable-blink-features=AutomationControlled")
#             options.add_argument("--disable-dev-shm-usage")
#             options.add_argument("--disable-gpu")
#             options.add_argument("--log-level=3")
#             options.add_argument("--disable-features=NetworkService,VizDisplayCompositor,UserAgentClientHint,HeaderClientHint")

#             # ✅ Set Randomized User-Agent
#             options.add_argument(f"user-agent={random.choice(self.user_agents)}")

#             # ✅ Use a Proxy to Rotate IP (Replace with a working proxy)
#             # options.add_argument("--proxy-server=http://your_proxy_here")

#             driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#             # ✅ Hide WebDriver Detection
#             driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#             driver.execute_script("window.navigator.chrome = { runtime: {} };")
#             driver.execute_script(
#                 "Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });"
#             )
#             driver.execute_script(
#                 "Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });"
#             )

#             # ✅ Simulate Human-like Interaction
#             driver.get(url)
#             time.sleep(random.uniform(3, 6))  # ✅ Randomized Delay

#             # Scroll like a human
#             for _ in range(random.randint(2, 4)):
#                 scroll_y = random.randint(300, 900)
#                 driver.execute_script(f"window.scrollBy(0, {scroll_y});")
#                 time.sleep(random.uniform(1, 3))

#             # Random clicks to appear more human
#             try:
#                 elements = driver.find_elements(By.TAG_NAME, "a")
#                 if elements:
#                     random.choice(elements).click()
#                     time.sleep(random.uniform(2, 5))
#             except:
#                 pass

#             return self._create_status(url, "UP", 200)

#         except WebDriverException as e:
#             logging.error(f"Selenium failed to load {url}: {e}")
#             return self._create_status(url, "DOWN", 500)

#         finally:
#             if "driver" in locals():
#                 driver.quit()

#     def _create_status(self, url, status, code):
#         """Create a status dictionary for the given site."""
#         return {
#             "url": url,
#             "status": status,
#             "status_code": code,
#             "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
#         }

#     def monitor_site(self, url):
#         """Continuously monitor sites in a separate thread."""
#         with self.lock:
#             if url in self.sites:
#                 logging.info(f"Already monitoring {url}")
#                 return

#             self.sites[url] = self._create_status(url, "INITIALIZING", 102)
#             logging.info(f"Current sites: {self.sites}")
#             self.socketio.emit("status_update", {"sites": list(self.sites.values())})

#         def monitoring_loop():
#             previous_status = None
#             while True:
#                 try:
#                     result = self.check_site_status(url)

#                     with self.lock:
#                         self.sites[url] = result

#                     if previous_status != result["status"]:
#                         logging.info(f"Site {url} changed to {result['status']}")
#                         result["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
#                         self.socketio.emit("status_update", {"sites": list(self.sites.values())})
#                         self.socketio.sleep(0)

#                         previous_status = result["status"]

#                 except Exception as e:
#                     logging.error(f"Monitoring error for {url}: {e}")

#                 self.socketio.sleep(10)

#         thread = threading.Thread(target=monitoring_loop, daemon=True)
#         thread.start()
# File: monitor.py
import requests
import logging
import random
import time
import threading
import undetected_chromedriver as uc

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from flask_socketio import SocketIO

# Configure logging: output to console and a log file.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler('monitor.log')]
)

class SiteMonitor:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.sites = {}
        self.lock = threading.Lock()
        self.driver_pool = []
        self.max_drivers = 3

        # User-Agent Rotation (Avoid bot detection)
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        ]

        # Optional: ChatGPT/DeepSeek specific selectors (update if needed)
        self.chatgpt_selectors = {
            # These selectors are examples—adjust them according to the actual page structure.
            "login_button": 'div[data-testid="login-button"]',
            "prompt_area": 'textarea#prompt-textarea'
        }

    def check_site_status(self, url):
        """Quickly check site status using requests, then fallback to Selenium if needed."""
        headers = {"User-Agent": random.choice(self.user_agents)}
        
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            status_code = response.status_code
            logging.info(f"Checked {url} - Status Code: {status_code}")

            # If site returns 403, assume bot detection and fallback to Selenium
            if status_code == 403:
                logging.warning(f"Bot detected via requests! Switching to Selenium for {url}")
                return self._selenium_check(url)

            # If status is 200-399, mark as UP
            if 200 <= status_code < 400:
                return self._create_status(url, "UP", status_code)

            return self._create_status(url, "DOWN", status_code)

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url}: {e}")
            return self._selenium_check(url)

    def _selenium_check(self, url):
        """Use undetected Selenium with advanced evasion techniques."""
        try:
            options = uc.ChromeOptions()
            options.add_argument("--headless=new")  # For Chrome 109+
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--log-level=3")
            options.add_argument("--disable-features=NetworkService,VizDisplayCompositor,UserAgentClientHint,HeaderClientHint")

            # Set Randomized User-Agent
            options.add_argument(f"user-agent={random.choice(self.user_agents)}")

            # Use a Proxy to Rotate IP (Replace with a working proxy)
            # options.add_argument("--proxy-server=http://your_proxy_here")

            driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            #  Hide WebDriver Detection
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("window.navigator.chrome = { runtime: {} };")
            driver.execute_script(
                "Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });"
            )
            driver.execute_script(
                "Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });"
            )

            # ✅ Simulate Human-like Interaction
            driver.get(url)
            time.sleep(random.uniform(1, 3))  # ✅ Randomized Delay

            # Scroll like a human
            for _ in range(random.randint(2, 4)):
                scroll_y = random.randint(300, 900)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
                time.sleep(random.uniform(1, 3))

            # Random clicks to appear more human
            try:
                elements = driver.find_elements(By.TAG_NAME, "a")
                if elements:
                    random.choice(elements).click()
                    time.sleep(random.uniform(1, 3))
            except:
                pass

            return self._create_status(url, "UP", 200)

        except WebDriverException as e:
            logging.error(f"Selenium failed to load {url}: {e}")
            return self._create_status(url, "DOWN", 500)

        finally:
            if "driver" in locals():
                driver.quit()

        


    def _verify_chatgpt(self, driver):
        """
        Special verification for ChatGPT/DeepSeek pages.
        Waits for the page to load and checks for common signs of access denial.
        """
        try:
            # Wait until the page is fully loaded (increase timeout if necessary)
            WebDriverWait(driver, 3).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Extra delay to allow dynamic content to load

            page_source = driver.page_source.lower()
            # Check for keywords indicating access denial or CAPTCHA challenges
            denial_keywords = ["access denied", "captcha", "blocked", "error 403", "cloudflare"]
            for keyword in denial_keywords:
                if keyword in page_source:
                    logging.warning(f"Detected denial keyword '{keyword}' in page source.")
                    return False

           
            # WebDriverWait(driver, 3).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, self.chatgpt_selectors["login_button"]))
            # )
            # WebDriverWait(driver, 3).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, self.chatgpt_selectors["prompt_area"]))
            # )

            return True
        except Exception as e:
            logging.error(f"ChatGPT verification failed: {e}")
            return False

    def _create_status(self, url, status, code):
        """Create a status dictionary for the given site."""
        return {
            "url": url,
            "status": status,
            "status_code": code,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def monitor_site(self, url):
        """Continuously monitor sites in a separate thread."""
        with self.lock:
            if url in self.sites:
                logging.info(f"Already monitoring {url}")
                return

            self.sites[url] = self._create_status(url, "INITIALIZING", 102)
            logging.info(f"Current sites: {self.sites}")
            self.socketio.emit("status_update", {"sites": list(self.sites.values())})

        def monitoring_loop():
            previous_status = None
            while True:
                try:
                    result = self.check_site_status(url)
                    with self.lock:
                        self.sites[url] = result

                    if previous_status != result["status"]:
                        logging.info(f"Site {url} changed to {result['status']}")
                        # Update the timestamp on each emission
                        result["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S')
                        self.socketio.emit("status_update", {"sites": list(self.sites.values())})
                        self.socketio.sleep(0)  # Allows real-time updates
                        previous_status = result["status"]

                except Exception as e:
                    logging.error(f"Monitoring error for {url}: {e}")

                self.socketio.sleep(2)  # Non-blocking sleep

        threading.Thread(target=monitoring_loop, daemon=True).start()
