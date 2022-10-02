# Google Images Scraper
# *******************************
# Author:        Jonathan Diebel
# Creation date: 30.09.2022
# Last change:   02.10.2022

import io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.error import HTTPError
from urllib.request import urlretrieve
from datetime import datetime
import io
import time
import os

# Configure Parameters
# ********************
labels = ['parsley', 'chives']
additionalSearchTerms = ['', 'plant', 'leaves', 'garden']
maxImagesPerSearchTerm = 10
delay = 0.3
downloadPath = 'images/'
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
    wd = webdriver.Chrome(webdriverPath)

    # Open google image-search and search for label
    for lbl in labels:
        collectedURLs = set()
        for addTerm in additionalSearchTerms:
            combinedSearchTerm = (lbl + ' ' + addTerm).replace(' ', '+')
            url = 'https://www.google.de/search?q=' + str(combinedSearchTerm) + '&hl=en&sclient=img&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiZ9t3H1sH6AhXTUOUKHU0HDH4Q_AUoAXoECAEQAw&biw=1515&bih=1304'
            # Collect all original source links of the found images
            collectedURLs = collectedURLs.union(
                getImageURLsFromGoogle(wd, delay, url, maxImagesPerSearchTerm))
            # print(collectedURLs)    # Debug

        # Download the collected URLs for the current label
        for i, url in enumerate(collectedURLs):
            pathForImage = directoryPath + lbl + '/'
            fileName = lbl + '_' + str(i+1)
            downloadImage(url, pathForImage, fileName, verbose=True)
            time.sleep(delay)

    # Close driver for Chrome
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

    # Open URL in controlled browser window
    wd.get(url)

    # Loop over images and collect URLs
    imageURLs = set()
    skippedImages = 0

    while len(imageURLs) + skippedImages < maxImages:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(imageURLs) + skippedImages:maxImages]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in imageURLs:
                    maxImages += 1
                    skippedImages += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    imageURLs.add(image.get_attribute('src'))

    return imageURLs


# Download Image
# Downloads the image from a given WebURL
def downloadImage(url, pathForImage, fileName, verbose):
    try:
        urlretrieve(url, pathForImage + fileName + '.jpg')
        if verbose == True:
            time = datetime.now()
            curr_time = time.strftime('%H:%M:%S')
            print(f'The image: {fileName} downloaded successfully at {curr_time}.')
    except FileNotFoundError as err:
        # something wrong with local path
        print(f'Unable to save image due to\n: {str(err)}')
    except HTTPError as err:
        # something wrong with url
        print(f'Unable to download image due to\n: {str(err)}')


# Write functions in any order
if __name__ == '__main__':
    main()

# ******************************************************
# End of File