
# Flatmates Scraper

## Overview
This repository contains a Python script `Flatmates_Scraper.py`, which is designed to scrape rental property data from a specified website and update a Google Sheet with the information. The script runs automatically every Sunday at midnight (UTC) via a GitHub Actions workflow.

## Features
- Scrapes average room rent, people looking, and rooms offered from a given URL.
- Captures supply-demand data for various suburbs and postcodes.
- Updates the data to a Google Sheet for easy tracking and analysis.
- Automated execution through GitHub Actions.

## Requirements
The script requires Python 3.8, along with several dependencies listed in `requirements.txt`. To install these dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage
To use the scraper:
1. Ensure all dependencies are installed.
2. Set up Google Sheets API with appropriate credentials.
3. Provide a `.xlsx` file with Australian postcodes and localities in the same directory as the script.
4. Configure the `GSPREAD_CREDENTIALS` and `GOOGLE_SHEET_ID` environment variables with your Google Sheets credentials and the ID of the target sheet, respectively.

## GitHub Actions Workflow
The `.github/workflows/scrape_and_update.yml` file defines the GitHub Actions workflow that schedules the execution of the script. It is set to run weekly, but you can adjust the schedule by modifying the cron expression in the YAML file.

## Contributing
Contributions to this project are welcome. Please ensure to update tests as appropriate.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the creators and contributors of the `requests`, `BeautifulSoup`, and `gspread` libraries.
- This project is for educational purposes and not affiliated with any data sources it scrapes from.

## Disclaimer
This scraper is only intended for personal use and educational purposes. It should not be used for commercial purposes. Please respect the terms of service of the website being scraped.
