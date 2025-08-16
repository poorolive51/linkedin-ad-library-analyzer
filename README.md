# LinkedIn Ad Library Analysis Toolkit

This repository contains a set of Python scripts to fetch, analyze, and visualize ad data from the LinkedIn Ad Library, using Airbnb as a case study. These scripts accompany a blog post that explains how to use LinkedIn's Ad Library API.

## Features

*   **Authentication:** A script to handle the OAuth 2.0 flow for obtaining a LinkedIn API access token.
*   **Data Fetching:** A script to fetch all ads for a specific advertiser (e.g., Airbnb).
*   **Data Visualization:** A script to plot the ad impressions over time, distinguishing between different geographic locations.

## Prerequisites

*   Python 3.6+
*   The following Python libraries: `requests`, `pandas`, `plotly`, `python-dotenv`

You can install the required libraries using pip:

```bash
pip install requests pandas plotly python-dotenv
```

## Setup

1.  **Create a LinkedIn Developer Application:**
    *   Go to the [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps/new) and create a new application.
    *   Add the "Sign In with LinkedIn" and "Ad Library" products to your app.
    *   Note your `Client ID` and `Client Secret`.

2.  **Configure the Environment:**
    *   Create a file named `.env` in the root of this directory.
    *   Add your LinkedIn application credentials to the `.env` file:

    ```
    LINKEDIN_CLIENT_ID=your_client_id
    LINKEDIN_CLIENT_SECRET=your_client_secret
    ```

## Usage

The scripts are designed to be run in the following order:

### 1. Get an Access Token

Run the `get_linkedin_access_token.py` script to obtain an OAuth 2.0 access token.

```bash
python get_linkedin_access_token.py
```

This script will:
*   Open a browser window for you to log in to LinkedIn and authorize the application.
*   After authorization, the script will capture the authorization code and exchange it for an access token.
*   The access token will be automatically saved to your `.env` file as `LI_ACCESS_TOKEN`.

### 2. Fetch Ad Data

Run the `fetch_airbnb_linkedin_ads.py` script to download all of Airbnb's ads from the LinkedIn Ad Library.

```bash
python fetch_airbnb_linkedin_ads.py
```

This script will:
*   Use the `LI_ACCESS_TOKEN` from your `.env` file to authenticate with the API.
*   Fetch all ads for the specified advertiser (`airbnb` by default).
*   Save the ad data to a file named `airbnb_all_ads.json`.

### 3. Visualize Ad Impressions

Run the `plot_airbnb_ad_impressions.py` script to generate a plot of the ad impressions data.

```bash
python plot_airbnb_ad_impressions.py
```

This script will:
*   Read the `airbnb_all_ads.json` file.
*   Process the data to calculate daily ad impressions for different locations (Amsterdam vs. the rest of the Netherlands).
*   Generate an interactive plot using Plotly, which will be displayed in your browser.

## Scripts Overview

*   **`get_linkedin_access_token.py`**: Handles the 3-legged OAuth 2.0 flow to get an access token.
*   **`fetch_airbnb_linkedin_ads.py`**: Fetches all ads for a given advertiser and saves them to a JSON file.
*   **`plot_airbnb_ad_impressions.py`**: Visualizes the ad impression data from the fetched JSON file.

### Running the Jupyter Notebook

To ensure the Jupyter Notebook (`analysis.ipynb`) runs correctly, please follow these steps:

1.  **Navigate to the repository's root directory:**
    Open your terminal or command prompt and change your current directory to the root of this repository (`linkedin-ad-library-analyzer`). This is crucial because the notebook uses relative paths to locate necessary files like `.env` and to save data.

    ```bash
    cd /path/to/your/linkedin-ad-library-analyzer
    ```

2.  **Verify your current directory (Optional but Recommended):**
    Before launching Jupyter, you can quickly check if you are in the correct directory by looking for the `.env.example` and `requirements.txt` files.

    ```python
    import os

    # Check if the necessary files are present
    required_files = ['.env.example', 'requirements.txt']
    for f in required_files:
        if not os.path.exists(f):
            print(f"Error: Required file '{f}' not found. Please make sure you are running this notebook from the root directory of the repository.")
            # You might want to exit the notebook here in a real application
    ```

3.  **Launch Jupyter Notebook:**
    Once in the correct directory, launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

    Your web browser should open, displaying the contents of the repository. You can then click on `analysis.ipynb` to open and run the notebook.