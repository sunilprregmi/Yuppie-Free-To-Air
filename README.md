# Yuppie Free-To-Air Channel Scraper

This project scrapes Free-To-Air (FTA) TV channel data from YuppTV and generates:
- `yuppie-fta.json`: A structured JSON file containing categorized channel information.
- `yuppie-fta.m3u8`: An M3U8 playlist for use in IPTV players.

## Features

- Fetches live channel data from YuppTV's public API.
- Outputs both a categorized JSON and a ready-to-use M3U8 playlist.
- Automatically updates daily at 10:00 AM Kathmandu time via GitHub Actions.

## Usage

### Requirements

- Python 3.7+
- `requests` library (see `requirements.txt`)

### Manual Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Run the script:
    ```bash
    python yuppie-fta.py
    ```
   This will generate or update `yuppie-fta.json` and `yuppie-fta.m3u8` in the project directory.

### Automated Updates

This repository includes a GitHub Actions workflow (`.github/workflows/daily-run.yml`) that:
- Runs the scraper every day at 10:00 AM Kathmandu time (UTC+5:45).
- Commits and pushes any changes to the JSON and M3U8 files automatically.

No manual intervention is needed for daily updates.

## Files

- `yuppie-fta.py` &mdash; Main script for scraping and generating outputs.
- `requirements.txt` &mdash; Python dependencies.
- `yuppie-fta.json` &mdash; Output: categorized channel data.
- `yuppie-fta.m3u8` &mdash; Output: IPTV playlist.
- `.github/workflows/daily-run.yml` &mdash; GitHub Actions workflow for automation.

## License

This project is for educational and personal use only. Please respect the terms of service of YuppTV and related content providers.

---

*Scrapped by @sunilprregmi*