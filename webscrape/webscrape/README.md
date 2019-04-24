# WebScrape Programme

## Requirements:
* [python 3](https://www.python.org/download/releases/3.0/)
* [node.js](https://nodejs.org/en/)
* [Lighthouse](https://www.npmjs.com/package/lighthouse)
* [requests](https://2.python-requests.org//en/master/)
* [tqdm](https://github.com/tqdm/tqdm)
* [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [pandas](https://pandas.pydata.org/)
* [xlsxwriter](https://xlsxwriter.readthedocs.io/)

## Installation:
Install python and the programme dependencies using the cli command:

`pip install <package name>` e.g `pip install tqdm` to install tqdm

Lighthouse is installed using the npm package manager and the command:

`npm install -g lighthouse` to install it globally on your system.

## Usage:
Run the main.py file and follow the steps. You can either run the scraper
by pressing 1 or change programme settings by pressing 2.

The programme will prompt the user to enter their desired query and the
number of search results you would like to obtain.

## Lighthouse Integration
Page performance is taken from using the *node.js* package *Lighthouse* to test
page load speeds in a headless chrome browser. This is called from the programme in
a call to the command line.

## Code Tips
All Functions and methods have been documented. If you look at the code in vscode
and hover over the function calls it will give you a quick description of the
function and what parameters it takes.

## Extension
### App Specific
More settings can be added to the *settings.json* file in the config directory to customise
the experience of the scraper even further.
## Lighthouse Specific
The lighthouse configuration can be altered in the *lighthouse.json* directory to what data
is contained in report. Currently it is only configured to give data for the performance
metrics of a webpage.

For more information on the configuration process and lighthouse in general check out the links
below:

* [https://github.com/GoogleChrome/lighthouse/blob/master/docs/scoring.md](https://github.com/GoogleChrome/lighthouse/blob/master/docs/scoring.md)
* [https://github.com/GoogleChrome/lighthouse/blob/master/docs/configuration.md](https://github.com/GoogleChrome/lighthouse/blob/master/docs/configuration.md)

## Issues
* Lighthouse requires that a protocol be present for testing a webpage speed
as a result some pages will fail and this will be shown through a `N/A` in the
data.

## Things That Could Be Done
* Could add a timer that shows when it can be used again.
* Could make the addition of additional choices dynamic.
* Use of arrays rather than lists to store data, could be faster.


