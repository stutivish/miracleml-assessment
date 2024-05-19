import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd

def retry_wrapper(func, max_retries=3, sleep_time=2):
    def wrapper(*args, **kwargs):
        for _ in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Failed with error: {e}")
                if _ == max_retries - 1:
                    print("Maximum retries reached. Aborting.")
                    return None
                print("Retrying...")
                time.sleep(sleep_time)
    return wrapper

@retry_wrapper
def download_csv_step1(driver):
    url = 'https://www.clinicaltrialsregister.eu/ctr-search/search?query='
    
    # Navigate to the Eudract search results page
    driver.get(url)

@retry_wrapper
def download_csv_step2(driver):
    wait = WebDriverWait(driver, 20)

    # Click on the download button 
    export_button_xpath = "//*[@id='submit-download']"
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, export_button_xpath)))
    export_button.click()

def read_text_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def convert_to_csv(file_path):
    # Read the downloaded text file 
    text = read_text_from_file(file_path)

    trials = text.strip().split('\n\n')
    csv_trials = []

    for trial in trials: 
        csv_trial = {}
        lines = trial.split('\n')
        for line in lines: 
            parts = [part.strip() for part in line.split(':', 1)]
            if len(parts) == 2:
                key = parts[0]
                value = parts[1]
                csv_trial[key] = value
            else: 
                break
        csv_trials.append(csv_trial)

    # df = pd.read_fwf(file_path)
    df = pd.DataFrame(csv_trials)

    # Save the DataFrame as CSV
    csv_path = os.path.splitext(file_path)[0] + '.csv'  # Replace extension with '.csv'
    df.to_csv(csv_path, index=False)
    print(f"Converted to CSV: {csv_path}")

def download_csv():    
    # Set up the WebDriver (Chrome in this case)
    options = webdriver.ChromeOptions()
    download_dir = os.path.abspath(f"data/eudract/{datetime.now().strftime('%Y%m%d%H%M%S')}")
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    download_csv_step1(driver)
    download_csv_step2(driver)
    
    # Wait for the download to complete
    time.sleep(20)

    # Find the downloaded text file
    files = os.listdir(download_dir)
    if files:
        file_path = os.path.join(download_dir, files[0])
        convert_to_csv(file_path)
    else:
        print("No files found in download directory.")
    
    driver.quit()
    
    return download_dir

if __name__ == "__main__":
    download_csv()
