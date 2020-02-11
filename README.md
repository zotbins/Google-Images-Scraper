# Google-Images-Scraper
## About
This is a selenium dynamic web page scraper to extract image URLs and download them to the local machine. This was originally intended to
collect training data for the ZotBins waste image recognition project, but could be used for other purposes.  
The script will download up to 400 images for a given search term. Runtime can vary depending on physical machine power and internet
latency. During testing, the script would complete in 3-4 minutes for a single search term.
## Prerequisites
* Python: (tested on version 3.6.5)
* Mozilla Firefox (tested on version 72.0.2)
* Setup selenium: https://selenium-python.readthedocs.io/installation.html
* only tested on Windows 10
## Running the script
```
python download_images.py <search terms>
```
For example, to download images for utensils and water bottles, run:
```
python download_images.py utensils "water bottles"
```
Remember to enclose multi-word arguments in quotes.
## Limitations
Web scraping is by nature dependent on the target. Therefore, any updates on google images may invalidate the script. View the 
`download_images.py` script documentation to see what can be done to keep the script updated.
## Common errors
#### Element could not be scrolled into view
During testing, we encountered the following error a few times:
```
selenium.common.exceptions.ElementNotInteractableException: Message: Element <option> could not be scrolled into view.
```
Somehow, we recieved the error the first one or two times we ran the scripts, and running the script afterwards did not reproduce
the error.  
We suggest that users who run into this error just run the script multiple times, and hopefully the error will disappear. The cause of 
this error is still unknown...
