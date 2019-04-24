import html
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from utils import utils

class Scraper(object):
    """Class for doing some google web scraping (allegedly)"""

    # google query string template
    query_string = "https://www.google.com/search?q={}&num={}"
    # lighthouse cli command template
    lighthouse_string = "lighthouse {} --output json --chrome-flags=\"--headless\" --config-path config/lighthouse.json"

    # class variables that are lists for data points
    query_links = []
    query_titles = []
    canon_links = []
    page_score = []
    query_metadata = []
    protocol = []
    status_codes = []
    h1_links = []
    h2_links = []

    def __init__(self, query, result_numb, user_agent):
        """ Scraper Constructor

        Parameters:
            query: String of desired query
            result_numb: number of results to get from google
            user_agent: string containing the user agent
        """
        self.query = query
        self.result_numb = result_numb
        self.user_agent = {"User-agent": user_agent}

    def scrape(self):
        """ Starts the scraping process for the data provided"""
        string = self.query_string.format(
            utils.querify_string(self.query), self.result_numb)
        try:
            # adds a user agent to requests if available.
            if self.user_agent["User-agent"] != None:
                query = requests.get(string, headers=self.user_agent)
            else:
                query = requests.get(string)
        except requests.RequestException:
            raise Exception("No Internet Connection")
        except requests.HTTPError:
            raise Exception("Google Has Blocked You")

        # prints status code for the request
        print("Status Code: {}".format(query.status_code))

        # parses the html data and find results tags

        html = query.text
        soup = BeautifulSoup(html, "html.parser")
        google_results = soup.find_all("div", {"class": "g"})

        print("Fetching Data From Specified Query")

        # will loop over results with progress bar -> (tqdm wrapping loop)
        for i in tqdm(range(len(google_results))):
            # link data
            link = google_results[i].find("a", href=True)["href"]
            self.query_links.append(utils.get_link_info(link))
            # various google result elements
            self.save_result_elements(google_results[i])
            # protocol
            self.protocol.append(self.getProtocol(self.query_links[i]))
            # various page elements (h1, h2, status_code)
            self.save_elements(self.query_links[i])
            # page score
            self.page_score.append(self.get_score(self.query_links[i]))

    def save_result_elements(self, result):
        """Gets elements from google search results

        Parameters:
            result: takes in the google result to parse elements
        """
        try:
            title = result.find("h3").text
        except AttributeError:
            title = "N/A"
        self.query_titles.append(title)

        try:
            metadata = result.find("span", {"class": "st"}).text
        except AttributeError:
            metadata = "N/A"
        self.query_metadata.append(metadata)

        try:
            canonical = result.cite.text
        except AttributeError:
            canonical = "N/A"
        self.canon_links.append(canonical)

    def save_elements(self, link):
        """Gets elements and status code from a specific webpage

        Parameters:
            link: a link of the google search result
        """
        try:
            if self.user_agent["User-agent"] != None:
                link_query = requests.get(
                    link, headers = self.user_agent)
            else:
                link_query = requests.get(link)
            self.status_codes.append(link_query.status_code)

            link_html = link_query.text
            link_soup = BeautifulSoup(link_html, "html.parser")
        except requests.RequestException:
            self.status_codes.append("N/A")
        else:
            # Find the h1 of page
            try:
                self.h1_links.append(link_soup.h1)
            except AttributeError:
                self.h1_links.append("N/A")
            # Find the h2 of page
            try:
                self.h2_links.append(link_soup.h2)
            except AttributeError:
                self.h2_links.append("N/A")

    def get_score(self, url):
        cli_call = self.lighthouse_string.format(url)
        # return the call from the command line as well as the status code
        call, status = utils.call_cli_command(cli_call)
        # if the status code is non zero i.e an error occured
        if status != 0:
            # makes the score not available
            score = "N/A"
        else:
            # decodes the bytes taken from call using the current encoding
            string_data = call.decode(utils.get_encoding())
            # takes the string data and makes it a python dictionary
            json_data = utils.load_json(string_data)
            # finds the sub key for the score value
            score = json_data["categories"]["performance"]["score"]
        return score

    def return_data_points(self):
        data = {
            "Link Number": [i + 1 for i in range(len(self.query_links))],
            "Query Titles": self.query_titles,
            "Query Links": self.query_links,
            "Canonical Links": self.canon_links,
            "Query Meta Desc": self.query_metadata,
            "Protocol": self.protocol,
            "Status Code": self.status_codes,
            "<h1>": self.h1_links,
            "<h2>": self.h2_links
        }
        return data

    @staticmethod
    def getProtocol(link):
        """ Checks the url protocol used for a given link

        Parameters:
            link: link string containing the protocol
        Returns:
            a statment representing what protocol the url uses.
        """
        if "https" in link:
            protocol = "Secured"
        else:
            protocol = "UnSecured"
        return protocol

    def save_results(self):
        raise NotImplementedError(
            "Method save_results not re-implemented into sub class")
