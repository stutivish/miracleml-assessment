import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

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
    url = 'https://clinicaltrials.gov/search'
    
    # Navigate to the ClinicalTrials.gov search results page
    driver.get(url)

@retry_wrapper
def download_csv_step2(driver):
    wait = WebDriverWait(driver, 20)

    # Click on the export button 
    export_button_xpath = "//*[@id='main-content']/ctg-search-results/div[2]/section/div[2]/div/div/div[2]/div/ctg-search-action-bar/div/div[1]/div[1]/ctg-download/button"
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, export_button_xpath)))
    export_button.click()

@retry_wrapper
def download_csv_step3(driver):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 20)
    
    # Limit results to top 10 
    top_button_xpath = "//*[@id='download']/div/div/div/div/div[1]/section[2]/div[4]/label"
    top_button = wait.until(EC.element_to_be_clickable((By.XPATH, top_button_xpath)))
    # Scroll the element into view
    actions.move_to_element(top_button).perform()
    top_button.click()

@retry_wrapper
def download_csv_step4(driver):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 20)
    
    # Click the Download button
    submit_button_xpath = "//*[@id='download']/div/div/div/div/div[2]/ul/li[1]/button"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    # Scroll the element into view
    actions.move_to_element(submit_button).perform()
    submit_button.click()

def download_csv():
    # url = 'https://clinicaltrials.gov/search'
    
    # Set up the WebDriver (Chrome in this case)
    options = webdriver.ChromeOptions()
    download_dir = os.path.abspath(f"data/clinical_trials/{datetime.now().strftime('%Y%m%d%H%M%S')}")
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Navigate to the ClinicalTrials.gov search results page
    # driver.get(url)

    # actions = ActionChains(driver)
    
    # # Click on the export button 
    # wait = WebDriverWait(driver, 20)
    # export_button_xpath = "//*[@id='main-content']/ctg-search-results/div[2]/section/div[2]/div/div/div[2]/div/ctg-search-action-bar/div/div[1]/div[1]/ctg-download/button"
    # export_button = wait.until(EC.element_to_be_clickable((By.XPATH, export_button_xpath)))
    # export_button.click()

    # # Limit results to top 10 
    # top_button_xpath = "//*[@id='download']/div/div/div/div/div[1]/section[2]/div[4]/label"
    # top_button = wait.until(EC.element_to_be_clickable((By.XPATH, top_button_xpath)))
    # # Scroll the element into view
    # actions.move_to_element(top_button).perform()
    # top_button.click()

    
    # # Click the Download button
    # submit_button_xpath = "//*[@id='download']/div/div/div/div/div[2]/ul/li[1]/button"
    # submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))
    # # Scroll the element into view
    # actions.move_to_element(submit_button).perform()
    # submit_button.click()

    download_csv_step1(driver)
    download_csv_step2(driver)
    download_csv_step3(driver)
    download_csv_step4(driver)
    
    # Wait for the download to complete
    time.sleep(20)
    
    driver.quit()
    
    return download_dir

if __name__ == "__main__":
    download_csv()