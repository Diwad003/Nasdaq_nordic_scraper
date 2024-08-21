import argparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def download_website(url, download_dir):
    # Set up Firefox options to specify the download directory
    options = Options()
    options.set_preference("browser.download.folderList", 2)  # Use custom download directory
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/html,application/xhtml+xml")

    # Initialize the Firefox browser using the WebDriver manager
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    # Open the specified URL
    driver.get(url)
    
    # Download the page (Save the webpage)
    with open(download_dir, 'w', encoding='utf-8') as outfile:
        outfile.write(driver.page_source)
    
    driver.quit()

    print(f"Website content from {url} has been saved to {download_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch content from a URL and process it.')
    parser.add_argument('input_url', type=str, help='The URL to fetch content from')
    parser.add_argument('output_file', type=str, help='The file to write the processed content to')

    args = parser.parse_args()

    download_website(args.input_url, args.output_file)