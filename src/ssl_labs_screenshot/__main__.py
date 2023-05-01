#!/usr/bin/env python3

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from urllib.parse import urlparse

VERSION = "v1.0.8"

def is_valid_domain(domain):
    try:
        parsed_domain = urlparse(domain)
        if parsed_domain.scheme in ["http", "https"]:
            domain = parsed_domain.netloc
        else:
            domain = parsed_domain.path
        if len(domain) > 0 and domain.count(".") > 0:
            # Remove any trailing slashes or path elements
            domain = domain.split('/')[0]
            return domain
    except Exception as e:
        return None
    return None

def main():
    print(f"SSL Labs Screenshot - Version {VERSION}")
    if len(sys.argv) < 2:
        print("Usage: python script.py domain.com")
        sys.exit(1)

    domain = sys.argv[1]

    sanitized_domain = is_valid_domain(domain)

    if not sanitized_domain:
        print("Invalid domain. Please enter a valid domain.")
        sys.exit(1)

    domain = sanitized_domain
    ssl_labs_url = f"https://www.ssllabs.com/ssltest/analyze.html?d={domain}&hideResults=on"

    print("Formatting and parsing the URL...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1200,1100")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("-n")
    chrome_options.add_argument("--guest")

    print("Setting up Chrome options...")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Launching Chrome driver...")
        driver.get(ssl_labs_url)

        print("Loading SSL Labs URL:", ssl_labs_url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "multiTable"))
            )
            print("Navigating to the first server's report...")
            first_server_link = driver.find_element(By.CSS_SELECTOR, "#multiTable a[href*='s=']").get_attribute("href")
            print("First server's report URL:", first_server_link)
            driver.get(first_server_link)
            WebDriverWait(driver, 220).until(
            EC.presence_of_element_located((By.ID, "rating"))
            )
        except:
            print("MultiTable not found, waiting for rating...")
            WebDriverWait(driver, 220).until(
                EC.presence_of_element_located((By.ID, "rating"))
            )

        # Hide all reportSection div elements except the first one
        driver.execute_script("""
            var reportSections = document.querySelectorAll('.reportSection');
            for (var i = 1; i < reportSections.length; i++) {
                reportSections[i].style.display = 'none';
            }
            var pageEnd = document.querySelector('#pageEnd');
            if (pageEnd) {
                pageEnd.parentNode.removeChild(pageEnd);
            }
        """)

        print("Capturing screenshot of the report...")
        driver.save_screenshot(f"{domain}_report_tmp.png")

        print(f"Screenshot saved as {domain}_report_tmp.png")

        # trim the image
        print("Trimming screenshot of the report...")
        image = Image.open(f"{domain}_report_tmp.png")
        image = image.convert('RGB')
        width, height = image.size
        background_color = image.getpixel((0, 0))
        left = width
        top = height
        right = 0
        bottom = 0
        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                if (r, g, b) != background_color:
                    if x < left:
                        left = x
                    if y < top:
                        top = y
                    if x > right:
                        right = x
                    if y > bottom:
                        bottom = y
        image = image.crop((left, top, right, bottom))
        image.save(f"{domain}_report.png")

        print(f"Trimmed screenshot saved as {domain}_report.png")

        # delete the tmp image
        os.remove(f"{domain}_report_tmp.png")

    finally:
        print("Quitting Chrome driver...")
        driver.quit()

if __name__ == "__main__":
    main()
