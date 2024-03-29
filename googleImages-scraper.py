# Google Images Scraper
# *******************************
# Author:        Jonathan Diebel
# Creation date: 30.09.2022
# Last change:   08.03.2023

from fileinput import filename
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
from urllib.error import HTTPError
from datetime import datetime
import func_timeout


# Configure Parameters
# ********************
labels = ['parsley', 'chives']
additionalSearchTerms = ['', 'plant', 'leaves', 'garden']
maxImagesPerSearchTerm = 10
searchLanguage = 'en'
delay = 0.2
downloadPath = 'F:/Development/images/'
# This script uses Selenium for automatic control of the Chrome browser. Please download the appropriate version here https://chromedriver.chromium.org/downloads and specify the path.
webdriverPath = 'F:/Development/GoogleImages-Scraper/chromedriver/chromedriver.exe'


# MAIN
# ********************
def main():
    # Check the length of the label list
    if len(labels) == 0:
        raise ValueError('The label list is empty.')

    # Check if Webdriver is provided
    if os.path.isfile(webdriverPath) == False:
        raise FileNotFoundError(
            'No Webdriver was found under the provided path.')

    # Create a folder for each lable to save the downloaded images
    time = datetime.now()
    currentTime = time.strftime('%b-%d-%Y_%H-%M-%S')
    directoryPath = downloadPath + currentTime + '/'
    # Make the directory if it doesn't exist
    for lbl in labels:
        if not os.path.exists(directoryPath + lbl):
            os.makedirs(directoryPath + lbl)
            print(f'Created directory: {str(lbl)}')

    # Set up driver for Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    wd = webdriver.Chrome(webdriverPath)
    wd.get('https://www.google.com/')
    # Close the cookie message if it is shown
    try:
        cookieButton = wd.find_element(By.ID, "W0wltc")
        cookieButton.click()
        print("Cookie message closed")
    except:
        pass

    # Open google image-search and search for label
    collectedURLs = set()
    for lbl in labels:
        collectedURLs.clear()
        for addTerm in additionalSearchTerms:
            print(f"Searching for: {lbl + ' ' + addTerm}")
            combinedSearchTerm = (lbl + ' ' + addTerm).replace(' ', '+')
            url = 'https://www.google.com/search?tbm=isch&q=' + str(combinedSearchTerm) + '&hl=' + str(searchLanguage)
            # Collect all original source links of the found images
            collectedURLs = collectedURLs.union(getImageURLsFromGoogle(wd, delay, url, maxImagesPerSearchTerm))
            #print(f'label: {lbl}, addTerm: {addTerm}, collectedURLs: {collectedURLs}')    # Debug

        # Download the collected URLs for the current label
        for i, url in enumerate(collectedURLs):
            pathForImage = directoryPath + lbl + '/'
            fileName = lbl + '_' + str(i+1)
            try:
                func_timeout.func_timeout(10, downloadImage, args=(url, pathForImage, fileName, True), kwargs=None)
            except func_timeout.FunctionTimedOut:
                print(f"Timeout while downloading {str(fileName)}: {url}")
                pass

    # Close driver for Chrome
    print("Downloading ended successfully.")
    wd.quit()


# FUNCTIONS
# ********************

# Get Image URLs from Google
# Get and list the image URLs from Google for a combinedSearchTerm
def getImageURLsFromGoogle(wd, delay, url, maxImages):
    # Function for scrolling down the page
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

        # Click "Show more results" button if it exists
        try:
            loadMoreButton = wd.find_element(By.CLASS_NAME, "mye4qd")
            loadMoreButton.click()
            print("'Show more results' button found")
        except:
            #print("No 'Show more results' button found")   # Debug
            pass

    # Open URL in controlled browser window
    url = url
    wd.get(url)

    # Loop over images and collect URLs
    imageURLs = set()
    skips = 0

    while len(imageURLs) + skips < maxImages:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        # Loop through each of the thumbnail images
        for img in thumbnails[len(imageURLs) + skips:maxImages]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            # Source the image URL link
            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for img in images:
                if img.get_attribute('src') in imageURLs:
                    maxImages += 1
                    skips += 1
                    break

                if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                    imageURLs.add(img.get_attribute('src'))

    return imageURLs


# Download Image
# Downloads the image from a given WebURL
def downloadImage(url, pathForImage, fileName, verbose):
    try:
        # Use headers to prevent HTTP 403 errors, occuring on some downloads. Ref: https://stackoverflow.com/a/45358832/6064933
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, pathForImage + fileName + '.jpg')
        if verbose == True:
            time = datetime.now()
            curr_time = time.strftime('%H:%M:%S')
            print(f'The image: {fileName} downloaded successfully at {curr_time}.')
    except FileNotFoundError as err:
        # something wrong with local path
        print(f'Unable to save image due to\n: {str(err)}')
        print(f'File path and name of the image: {pathForImage + fileName}')
    except HTTPError as err:
        # something wrong with url
        print(f'Unable to download image due to\n: {str(err)}')
        print(f'URL of the image: {url}')
    except:
        # unhandled error
        print(f'Unable to download image due to unhandled error')
        print(f'URL of the image: {url}')

    return None


# Write functions in any order
if __name__ == '__main__':
    main()

# ******************************************************
# End of File