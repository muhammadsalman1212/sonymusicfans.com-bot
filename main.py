import glob
import json
import os
import random
import time
import shutil
from pathlib import Path
import csv
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
# pip install playwright
# playwright install
# pip install pandas, requests
import time
import random



# Load ZIP code data (ensure you have a CSV with valid ZIP codes)
data = pd.read_csv('USzipcodes.csv')  # Replace with your dataset file
zip_codes_list = data['zip_code'].tolist()

emails_csv = pd.read_csv('emails.csv')  # Replace with your dataset file
emails_data_list = emails_csv['Emails'].tolist()
print(emails_data_list)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    count = 1
    for all_emails in emails_data_list:
        print(f"Submitting email {count} of {len(emails_data_list)}")
        page.goto("https://forms.sonymusicfans.com/campaign/acdc-officialnewsletter/", timeout=0)

        # fill the full name
        fill_full_name = page.fill('//input[@id="field_first_name"]', "John Doe", timeout=0)

        # fill the email
        fill_email = page.fill('//input[@name="field_email_address"]', all_emails)

        # click on tap to continue button
        taptocontinue_btn = page.click("//span[normalize-space()='Tap to Continue']", timeout=0)

        time.sleep(3)

        values_list = ['1517', '1822', '2326', '2730', '3135', '3640', '4145', '4651', '5260', '6170', '7180']
        random_value = random.choice(values_list)
        dropdown_selector = "#field_age_range"
        value_to_select = random_value

        page.wait_for_selector(dropdown_selector)
        page.select_option(dropdown_selector, value_to_select)

        country_dropdown_xpath = '//select[@id="field_country_region"]'

        # The country code for "United States" is "US"
        target_country = "US"

        # Select "United States" by its value
        page.locator(country_dropdown_xpath).select_option(value=target_country)


        # random zip code
        random_value = random.choice(zip_codes_list)
        zip_code_input = '//input[@name="field_postal_code"]'
        fill_thezipcode = page.fill(zip_code_input, str(random_value), timeout=0)

        # click on tap to finish button

        page.click("//span[normalize-space()='Tap to Finsh']", timeout=0)
        count += 1

        header = ['Done-process-emails']
        with open('done_emails.csv', 'a+', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if file is empty
                writer.writerow(header)
            writer.writerow([all_emails])


        time.sleep(5)

    print("All emails submitted successfully.")
    page.close()


