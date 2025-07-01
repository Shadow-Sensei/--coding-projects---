i will paste everything here 



# Quote Scraper

A web scraper that uses selenium to extract quotes from "https://quotes.toscrape.com".
It handles pagination and saves the data to a CSV file using 'pandas'.


## Features
- Uses Selenium Webdriver with Firefox 
- Handles pagination automatically 
- Saves quotes to a structured CSV file 
- Logs activity with timestamps 


## Requirements
- Python 3.8+
- Firefox installed
- geckodriver (for Firefox WebDriver)


## Installation

### 1. Clone the repository:
``` bash 
git clone https://github.com/Shadow-Sensei/--coding-projects---.git
cd coding-projects/quote_scraper_selenium
python3 main.py
```

### 2. Install Dependencies:
Make sure you are inside a virtual environment
``` bash
pip install -r requirements.txt
```
### 3. Install geckodriver:

(Arch Linux) -
```bash
 sudo pacman -S geckodriver
```
(Ubuntu/Debian)
``` bash
             sudo apt update
             sudo apt install firefox-geckodriver
```
if firefox-geckodriver isn't available:
``` bash
     sudo apt install wget

    wget https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-linux64.tar.gz

     tar -xvzf geckodriver-linux64.tar.gz

     sudo mv geckodriver /usr/local/bin/
```

(macOS with Homebrew):
``` bash
brew install geckodriver
```
if you don't have Homebrew:

paste this in the terminal:
``` bash
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
 ```

(For Windows):

1.Go to: https://github.com/mozilla/geckodriver/releases

2.Download the latest .zip for Windows 64-bit

3.Extract geckodriver.exe

4.Move it to a folder (e.g. C:\tools\geckodriver\)

5.Add that folder to your System PATH:

6.Search for "Environment Variables"

7.Edit the Path variable

8.Add C:\tools\geckodriver\

9.Restart your terminal or IDE (VS Code, etc.)


Verify Installation:
type this in terminal or CMD:
geckodriver --version

### 4. How to run:
``` bash
python main.py
```
## Output
A quotes.csv file will be generated will all the quotes,authors,and tags from the website

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.