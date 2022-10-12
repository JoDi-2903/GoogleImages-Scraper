# GoogleImages-Scraper
Tool to download images from Google Image Search based on given set of keywords for training machine learning models.
<br/>
<h2>Description</h2>
The "GoogleImages-Scraper" is a tool for automatic download of photos from Google Image Search. The script downloads and saves the photos sorted by labels and is suitable for generating training data for machine learning models. The parameters can be used to configure different labels, search term combinations, maximum number of images, delay as well as the download path. The photos are sorted by their labels into subfolders.

<h2>Example configuration for parameters</h2>

```python
labels = ['parsley', 'chives']
additionalSearchTerms = ['', 'plant', 'leaves', 'garden']
maxImagesPerSearchTerm = 10
searchLanguage = 'en'
delay = 0.2
downloadPath = 'F:/Development/images/'
webdriverPath = 'F:/Development/GoogleImages-Scraper/chromedriver/chromedriver.exe'
```

<h2>Required packages</h2>

* selenium 4.5.0 
* urllib3 1.26.12 
* DateTime 4.7
* func-timeout 4.3.5

The `requirements.txt` file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

<h2>Download webdriver for Selenium</h2>
This script uses Selenium and WebDriver for automatic control of the Chrome browser. WebDriver is an open source tool for automated testing of webapps across many browsers. It provides capabilities for navigating to web pages, user input, JavaScript execution, and more.  ChromeDriver is a standalone server that implements the W3C WebDriver standard. ChromeDriver is available for Chrome on Android and Chrome on Desktop (Mac, Linux, Windows and ChromeOS).
<br><br>
Please download the appropriate version at https://chromedriver.chromium.org/downloads and specify the path as parameter in the python script.
