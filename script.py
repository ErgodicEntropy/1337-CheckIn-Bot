import os
import random
import time
import json
import winsound
import requests
import webbrowser
# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support.ui import WebDriverWait
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.support import expected_conditions as EC


WEBHOOK_URL = os.getenv("WEBHOOK_URL")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# webhook
def send_discord_alert(message):
    url = WEBHOOK_URL
    payload = {
        "content": message,
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Discord alert sent successfully!")
        else:
            print(f"❌ Failed to send alert: {response.text}")
    except Exception as e:
        print(f"❌ Error sending Telegram alert: {e}")



# Auto Login

LOGIN_URL = "https://admission.1337.ma/users/sign_in"

def autologin(driver, wait): 

    driver.get(LOGIN_URL)
    
    #wait until the input elements appear in the DOM (otherwise NoSuchElementException pops up due to mistiming issues)
    wait.until(
            EC.presence_of_element_locaetd((By.CSS_SELECTOR, "input[type='email']"))
    )

    email_input = driver.find_element(by=By.CSS_SELECTOR, value="input[name='email']") 
    
    wait.until(
            EC.presence_of_element_locaetd((By.NAME, "password"))
    )
    
    password_input = driver.find_element(By.NAME, "password")   

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    
    # password_input.send_keys(Keys.Enter)
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    time.sleep(1)
    
    save_cookies(driver)
    
def is_login(driver):    
    return 'sign_in' not in driver.current_url.lower() 

def save_cookies(driver):
    json.dump(driver.get_cookies(), open("cookies.json", "w")) #can access cookies even if HttpOnly is true (unlike document.cookie)

def load_cookies(driver): 
    with open("cookies.json", "r") as f:
        cookies = json.load(f) #driver.add_cookies(cookies) can do
        for cookie in cookies: 
                driver.add_cookie(cookie)  

#Catpcha Detection

def detect_recaptcha_v2(driver): # google ReCATPCHA detection
    try:          
        target_iframe = None
        
        iframes = driver.find_elements("tag name", "iframe")
        for iframe in iframes:
            driver.implicitly_wait(3)
            src = iframe.get_attribute("src") or ""
            if "recaptcha" in src:
                target_iframe = iframe
                break
                            
        return target_iframe
    except NoSuchElementException:
        return False
    
# Captcha Resolution

def solve_recaptcha_v2_checkbox(driver, recaptcha_iframe): #I'm not a robot' (check the box) resolution (but can solve any other ReCATPCHA type)
    try:
        solver = RecaptchaSolver(driver=driver)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        
        print("[✓] reCAPTCHA solved successfully!")

        return True
        
    except Exception as e:
        print(f"[✗] Failed to solve reCAPTCHA: {str(e)}")
        return False


# Captcha Verification

def verify_recaptcha_v2_checkbox(driver, recaptcha_iframe):
    driver.switch_to.frame(recaptcha_iframe) #switch to the iframe to be able to access the checkbox element of the inserted/embedded document from another domain

    checkbox = driver.find_element(By.ID, "recaptcha-anchor")
    if "recaptcha-checkbox-checked" in checkbox.get_attribute("class") or "":
        print("[✓] reCAPTCHA verified successfully! 1")
        return True

    driver.switch_to.default_content()
    
    # when the g-captcha is solved, the textarea is filled with a CAPTCHA token that the site sends to its backend
    textarea = driver.find_element(By.CLASS_NAME, "g-recaptcha-response")
    value = textarea.get_attribute("value") or ""
    if (value):
        print("[✓] reCAPTCHA verified successfully! 2")
        return True
    
    return False

    
# Register Button

def register_checkin(wait):
    try:        
        input = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit']"))
        )

        if (input.get_attribute("value") == "Submit"):
            input.click()
            print("Check-In Booked! 1")
            return True

        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )

        if (button.get_attribute("value") == "Submit"):
            button.click()
            print("Check-In Booked! 2")
            return True
        
    except NoSuchElementException as e:
        print(f"error: {e}")
        return False


#MAIN

options = uc.ChromeOptions()
options.page_load_strategy = 'normal' #complete page loading (still not sufficient to prevent synchronization gaps between the actual DOM and the Selenium DOM snapshot)

options.proxy = Proxy({ 'proxyType': ProxyType.MANUAL, 'httpProxy' : 'http.proxy:1234'}) #to get around restriction policies or complex network topologies
options.browser_version = 'stable'
options.platform_name = 'any'

options.add_argument("--no-sandbox")               # Disables Chrome sandbox for Docker/Linux compatibility
options.add_argument("--disable-dev-shm-usage")    # Prevents /dev/shm crashes in Docker containers
options.add_argument("--disable-blink-features=AutomationControlled") # Hides automation to avoid bot detection
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")  # Spoofs regular Chrome browser
options.add_argument("--no-first-run")             # Skips Chrome welcome/setup pages on first launch
options.add_argument("--no-service-autorun")       # Prevents background services like auto-updates
options.add_argument("--password-store=basic")     # Uses plaintext password storage to avoid keyring popups
options.headless = False                           # Runs browser in visible mode (easier for debugging)
options.add_argument("--disable-webrtc")           # Prevents IP leaks through WebRTC
options.add_argument("--disable-gpu")              # Helps with stability in some environments
options.add_argument("--window-size=1920,1080")    # Sets consistent viewport size
options.add_argument("--start-maximized")          # Starts with maximized window

driver = uc.Chrome(options=options)  # Forces ChromeDriver 146.x.x.x if you so neeed

errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, timeout=10, poll_frequency=2, ignored_exceptions=errors)


autologin(driver)

load_cookies(driver)

driver.get("https://admission.1337.ma/candidature/check-in")

input("Press Enter to start monitoring for ReCAPTCHA...")

try:
    while True:
        wait.until(
            EC.invisibility_of_element((By.CSS_SELECTOR, ".animate-spin")) #Wait for the Loading spinner SVG to disappear or gets removed from the DOM
        )
        if not is_login(driver):
            autologin(driver, wait) #login and save new cookies (overwrite the previous cookies)
            load_cookies(driver) 
        recaptcha_iframe = detect_recaptcha_v2(driver)
        if recaptcha_iframe:
            print("[*] reCAPTCHA detected!")
            winsound.Beep(1000,2000) #windows beep
            send_discord_alert("🚨 1337 CHECK-IN AVAILABLE! Click NOW: https://admission.1337.ma/candidature/check-in") #discord webhook notification automation system
            webbrowser.open_new("https://admission.1337.ma/candidature/check-in") #open the link automatically in a new tab (this assumes cfclearance and accessToken, stored in the domain cookie, are valid and didn't change values)
            time.sleep(5)
            if solve_recaptcha_v2_checkbox(driver,recaptcha_iframe):
                if verify_recaptcha_v2_checkbox(driver,recaptcha_iframe):
                    register_checkin(wait)
            time.sleep(5)
            break
        else:
            print("[+] No CAPTCHA detected")
            import random
            b = random.random()
            if b > 0.95: #shorter wait (impatient 5% of the time)
                time.sleep(random.uniform(3,5))
            elif b > 0.75: #longer wait (distraction 20% of the time)
                time.sleep(random.uniform(10,13))  
            else: #normal behavior (75% of the time)
                time.sleep(max(0,random.gauss(mu=8,sigma=2)))
            driver.refresh()


except Exception as e:
    print(f"Error {e}")

finally:
    try:    
        driver.quit()
    except:
        pass
