# miracleml-assessment

# Data Pipeline Setup

## Overview
This repo contains the setup instructions and code for a data pipeline that automates the process of scraping, storing, and visualizing data.

## Components
The data pipeline consists of the following components:
1. **Data Sources**: ClinicalTrials.gov and Eudract
2. **Data Collection**: Python scripts that utilize `selenium` to perform web scraping of data by simulating user actions like clicking on an export or download button. 
3. **Data Processing**: Python scripts to clean, transform, and manipulate the raw data into a usable format. Libraries used for this was `pandas`.
4. **Data Storage**: Data is stored in a local database using `PostgreSQL`.
5. **Scheduling Scripts**: For this project, I used a simple `schedule` python library to call the script every hour. However, cloud deployed cron jobs are likely better practice.
6. **Web App to Visualize Data**: Utilized React, Node.js, and Express to create a web app. `express` was used for defining apis to query data from postgres tables. APIs were called from frontend to retrieve data and `React` components were defined to visualize the data. Also utilized `d3.js` to create a chart visual.

## Setup Instructions
1. **Clone the Repository**: Clone this repository to your local machine.
    ```bash
    git clone https://github.com/stutivish/miracleml-assessment.git
    ```
2. **Install Dependencies**: Install the necessary dependencies. Use a virtual environment if needed.
    ```
    cd scraper/
    pip3 install -r requirements.txt
    ```

    ```
    cd server/
    npm install
    ```

    ```
    cd client/
    npm install
    ```

    Ensure that you have postgresql@14. Install if you do not already have it.
    ```
    brew upgrade
    brew doctor
    brew install postgresql@14
    ```
3. **Database Setup**:
    Create the Database
    ```
    createdb clinical_trials
    ```

    Ensure your database has been created properly by doing
    ```
    psql -d clinical_trials
    ```

    Populate the database with tables using the `db/db_setup.sql` file
    ```
    psql -d clinical_trials -f db/db_setup.sql 
    ```

4. **Run the Project**: 
    You will need to have 3 terminal tabs open. One for each directory: `scraper`, `client`, `server`.

    In `scraper` directory:
    Execute the main script to scrape the data. This will create a pop up on the screen as it it's simulating user actions on Chrome. This is scheduled to call every hour by default. This will save local files of data and insert it into database tables.
        ```
        python3 scraper.py
        ```

    In `server` directory: 
    This will start the backend server on port 8080
        ```
        node index.js
        ```
    
    In `client` directory: 
    This will start your local web application at localhost:3000
        ```
        npm run start
        ```
