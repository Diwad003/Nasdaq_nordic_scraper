import argparse
import os
import sys
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

def get_company_name(url, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        lines = [line for line in r.text.splitlines() if line.strip() != ""]
        lines = lines[593:]
        for i in range(len(lines)):
            if lines[i] == "<tr>":
                i += 1
                outputForwardLink = extract_between_value(lines[i], '"', '&')

                i += 1
                outputCompanySymbol = extract_between_value(lines[i], '>', '<')
                fpName = f"{dir}/{outputCompanySymbol}.txt"
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
    else:
        print("FAIL CANNOT CONNECT")
        sys.exit(1)
    
    print("Program has extracted all useful information from %s and put it into individual files in %s" % (url, dir))
    

def extract_between_value(string, first_separator, end_separator):
    start = string.find(first_separator)
    if start != -1:
        start += len(first_separator)
        end = string.find(end_separator, start)
        if end != -1:
            return string[start:end]
    return None

def get_company_info(dir):
    dir_list = os.listdir(dir)
    for textfile in dir_list:
        combineDir = dir + textfile
        outfile = open(combineDir, 'r', encoding='utf-8')
        str = outfile.readline()
        outfile.close()

        websiteLink = [line for line in str.splitlines() if line.strip()]
        websiteLink = "https://www.nasdaqomxnordic.com" + websiteLink[0]
        print(websiteLink)
        price, shares, volume, numTrades = download_website(websiteLink)

        outfile = open(combineDir, 'a', encoding='utf-8')
        outfile.write("%s\n%s\n%s\n%s\n" % (price, shares, volume, numTrades))
        outfile.close()

        
def download_website(url):
    options = Options()
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(2)  # Wait for the page to fully load

    lines = [line for line in driver.page_source.splitlines() if line.strip()]
    #with open("temp.txt", 'w', encoding='utf-8') as outfile:
    #    for line in lines:
    #        outfile.write(line + '\n') 
    driver.quit()
    

    outputPrice = extract_between_value(lines[552], ">", "<")
    outputShares = extract_between_value(lines[561], r'nos">', "</span")
    outputVolume = extract_between_value(lines[619], r'"tv">', "</span>")
    outputNumberOfTrades = extract_between_value(lines[627], r'"not">', "</span>")

    priceString = outputPrice.replace(',', '', 1)
    priceInt = float(priceString.replace(',', '.'))
    
    sharesInt = 0
    volumeInt = 0
    volumeNumTrades = 0
    if outputShares and outputShares != "&nbsp;":
        sharesInt = int(outputShares.replace(',', ''))
    if outputVolume and outputVolume != "&nbsp;":
        volumeInt = int(outputVolume.replace(',', ''))
    if outputNumberOfTrades and outputNumberOfTrades != "&nbsp;":
        volumeNumTrades = int(outputNumberOfTrades.replace(',', ''))

    print("\n")
    print(priceInt)
    print(sharesInt)
    print(volumeInt)
    print(volumeNumTrades)
    print("\n")

    if not isinstance(priceInt, float) or not isinstance(sharesInt, int) or not isinstance(volumeInt, int):
        print("Price, shares eller volume är inte ints")
        exit(1)
    
    return priceInt, sharesInt, volumeInt, volumeNumTrades


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch content from a URL and process it.')
    parser.add_argument('input_url', type=str, help='The URL to fetch content from')
    parser.add_argument('directory', type=str, help='The URL to fetch content from')
    args = parser.parse_args()

    start = time.time()
    get_company_name(args.input_url, args.directory) # https://www.nasdaqomxnordic.com/shares/listed-companies/stockholm
    get_company_info(args.directory)
    end = time.time()
    elapsed_time = end-start

    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    print(f"Time taken: {hours} hours, {minutes} minutes, and {seconds} seconds")