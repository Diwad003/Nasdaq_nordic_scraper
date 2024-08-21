import argparse
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

def get_company_name(url):
    r = requests.get(url, headers=HEADERS)
    sleep(1)

    if r.status_code == 200:
        lines = [line for line in r.text.splitlines() if line.strip() != ""]
        lines = lines[593:]        
        for i in range(len(lines)):
            if lines[i] == "<tr>":
                i += 1
                outputForwardLink = extract_between_value(lines[i], '"', '&')

                i += 1
                outputCompanySymbol = extract_between_value(lines[i], '>', '<')
                fpName = "info/%s.txt" % outputCompanySymbol
                fp = open(fpName, "w")
                fp.write("%s\n" % outputForwardLink)
                fp.write("%s\n" % outputCompanySymbol)

                i += 1
                outputCurrency = extract_between_value(lines[i], '>', '<')
                fp.write("%s\n" % outputCurrency)

                i += 1
                outputISIN = extract_between_value(lines[i], '>', '<')
                fp.write("%s\n" % outputISIN)

                i += 1
                outputSector = extract_between_value(lines[i], '>', '<')
                fp.write("%s\n" % outputSector)

                i += 1
                outputICB = extract_between_value(lines[i], '>', '<')
                fp.write("%s\n" % outputICB)

                fp.close()

    

def extract_between_value(string, first_separator, end_separator):
    start = string.find(first_separator)
    if start != -1:
        start += 1
        end = string.find(end_separator, start)
        if end != -1:
            return string[start:end]
    return None

def get_company_prices(url):
    options = Options()
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1,
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    sleep(2)

    lines = [line for line in driver.page_source.splitlines() if line.strip()]
    output = extract_between_value(lines[552], '>', '<')
    print(output) 

    with open("webhandle.txt", 'w', encoding='utf-8') as outfile:
        for line in lines:
            outfile.write(line + '\n')
    
    driver.quit()
    

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Fetch content from a URL and process it.')
    #parser.add_argument('input_url', type=str, help='The URL to fetch content from')
    #parser.add_argument('output_file', type=str, help='The file to write the processed content to')
    #args = parser.parse_args()

    get_company_name("https://www.nasdaqomxnordic.com/shares/listed-companies/stockholm")
    #get_company_prices()


