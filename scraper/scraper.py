import clinical_trial_scraper
import eudract_scraper
import os
import time
import psycopg2
import pandas as pd
import schedule

def insert_into_database(clinical_trial, eudract_download):
    connection = psycopg2.connect(
        host="localhost",
        user="stuti",
        dbname="clinical_trials"
    )
    
    try:
        with connection.cursor() as cursor:
            ctg_data = pd.read_csv(clinical_trial)

            # insert data into us table
            for index, row in ctg_data.iterrows():
                cursor.execute(
                    """
                    INSERT INTO us (study_id, study_title, conditions, sponsor)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (study_id) DO UPDATE SET
                    study_title = EXCLUDED.study_title,
                    conditions = EXCLUDED.conditions,
                    sponsor = EXCLUDED.sponsor
                    """,
                    (row['NCT Number'], row['Study Title'], row['Conditions'], row['Sponsor'])
                )
            
            # insert data in eu table
            eu_data = pd.read_csv(eudract_download)
            for index, row in eu_data.iterrows():
                cursor.execute(
                    """
                    INSERT INTO eu (study_id, study_title, conditions, sponsor)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (study_id) DO UPDATE SET
                    study_title = EXCLUDED.study_title,
                    conditions = EXCLUDED.conditions,
                    sponsor = EXCLUDED.sponsor
                    """,
                    (row['EudraCT Number'], row['Full Title'], row['Medical condition'], row['Sponsor Name'])
                )

            # insert data into combined table
            cursor.execute(
                """
                INSERT INTO combined (study_id, study_title, conditions, sponsor)
                SELECT
                    CONCAT('US_', study_id) as study_id,
                    LOWER(study_title) as study_title,
                    conditions,
                    sponsor
                FROM us
                ON CONFLICT (study_id) DO UPDATE SET
                study_title = EXCLUDED.study_title,
                conditions = EXCLUDED.conditions,
                sponsor = EXCLUDED.sponsor;
                """
            )
            cursor.execute(
                """
                INSERT INTO combined (study_id, study_title, conditions, sponsor)
                SELECT
                    CONCAT('EU_', study_id) as study_id,
                    LOWER(study_title) as study_title,
                    conditions,
                    sponsor
                FROM eu
                ON CONFLICT (study_id) DO UPDATE SET
                study_title = EXCLUDED.study_title,
                conditions = EXCLUDED.conditions,
                sponsor = EXCLUDED.sponsor;
                """
            )

        connection.commit()
    finally:
        connection.close()

def scrape():
    clinical_trial = clinical_trial_scraper.download_csv()
    eudract_download = eudract_scraper.download_csv()

    # Wait until the CSV file is downloaded completely
    # Check if the CSV file exists in the download directory
    while not os.path.exists(clinical_trial) or not os.path.exists(eudract_download):
        time.sleep(1)  # Wait for 1 second

    clinical_trial_csv = os.path.join(clinical_trial, 'ctg-studies.csv')
    eudract_csv = os.path.join(eudract_download, 'trials-summary.csv')
    print("file1:", clinical_trial_csv)
    print("file 2:", eudract_csv)
    
    insert_into_database(clinical_trial_csv, eudract_csv)

if __name__ == "__main__":
    # Schedule the scraping function to run every 5 minutes
    schedule.every(3).minutes.do(scrape)
    # Run the scheduler indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage
