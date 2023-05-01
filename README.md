# SSL Labs Screenshot
A Python package to capture a trimmed screenshot of the SSL Labs report for a given domain.

<p align="center"><img src="https://raw.githubusercontent.com/marksowell/SSL-Labs-Screenshot/main/images/www.ssllabs.com_report.png" width="300px" />

## Requirements
- Python 3.6 or newer
- Chrome browser version 89 or later
- ChromeDriver

## Installation
1. Install using pip:

   ```
   pip install ssl-labs-screenshot
   ```
2. Download the latest version of ChromeDriver from the following link: https://sites.google.com/chromium.org/driver/downloads
3. Extract the contents of the downloaded ZIP file.
4. Either move the ChromeDriver executable to a directory that is already included in your system's `PATH` environment variable, or add the directory containing the extracted ChromeDriver executable to your system's `PATH` variable.

## Usage
Run the script with the following command:
```
ssl-labs-screenshot domain.com
```
Replace domain.com with the domain you want to test. The script will open a headless Chrome browser and load the SSL Labs report for the domain. It will capture a temporary screenshot of the report and save it as a PNG file in the same directory as the script, with the name domain_report_tmp.png. The script will delete the temporary screenshot after the trimmed image is created with the name domain_report.png

## Limitations
The script only captures the first server's report for domains with multiple servers.

## License
The scripts and documentation in this project are released under the [MIT License](https://github.com/marksowell/SSL-Labs-Screenshot/blob/main/LICENSE)