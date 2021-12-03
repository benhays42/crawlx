# CrawlX Crawler (c) Ben Hays 2021

# Imports
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup
import re
import time
import sys
import os
import argparse
import logging
import json
import urllib.parse


# Global Variables
CRAWLX_VERSION = "0.1.0 (beta)"
CRAWLX_DEFAULT_TIMEOUT = 10
CRAWLX_DEFAULT_MAX_DEPTH = 3
CRAWLX_DEFAULT_MAX_PAGES = 100
CRAWLX_DEFAULT_MAX_CONCURRENT_REQUESTS = 10
CRAWLX_DEFAULT_MAX_REQUESTS_PER_PAGE = 10
CRAWLX_DEFAULT_MAX_REQUESTS_PER_SECOND = 10
CRAWLX_DEFAULT_MAX_REQUESTS_PER_MINUTE = 60
CRAWLX_DEFAULT_MAX_REQUESTS_PER_HOUR = 3600
CRAWLX_DEFAULT_MAX_REQUESTS_PER_DAY = 86400

# Global Functions
def crawl(url, depth=CRAWLX_DEFAULT_MAX_DEPTH, max_urls=CRAWLX_DEFAULT_MAX_PAGES, timeout=CRAWLX_DEFAULT_TIMEOUT):
    found_links = []
    page = session.get(url, timeout=timeout)
    # Bs4 the home page
    soup = BeautifulSoup(page.result().content, 'html.parser')
    links = soup.find_all('a')
    forms = soup.find_all('form')
    cookies = page.result().cookies  
    headers = page.result().headers

    print("Found " + str(len(links)) + " links and " + str(len(forms)) + " forms")

    # Add the home page hrefs to the found links
    for link in links:
        found_links.append(link.get('href'))

    # Add the home page form action hrefs to the found links
    for form in forms:
        found_links.append(form.get('action'))

    # Search for links in the cookies by searching with regex
    for cookie in cookies:
        if re.findall(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', cookie.value):
            found_links.append(re.findall(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', cookie.value)[0])

    # Do the same with headers
    for header in headers:
        if re.findall(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', header):
            found_links.append(re.findall(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', header)[0])

    # Remove NoneType links
    for link in found_links:
        if link is None:
            found_links.remove(link)

    # Add schema to relative links
    for link in found_links:
        if link and link.startswith('/'):
            found_links.remove(link)
            #found_links.append(url + link)

    # Remove hash links
    for link in found_links:
        if link and link.startswith('#'):
            found_links.remove(link)

    # Remove out of scope links
    for link in found_links:
        if link and not link.startswith(url):
            found_links.remove(link)

    # Remove duplicates
    found_links = list(set(found_links))
    return found_links


# Handle Arguments with argparse
parser = argparse.ArgumentParser(description='CrawlX Crawler v' + CRAWLX_VERSION)
parser.add_argument('-u', '--url', help='URL to crawl', required=True)
parser.add_argument('-o', '--output', help='Output file', required=False)
parser.add_argument('-d', '--depth', help='Depth of crawl', required=False, default=CRAWLX_DEFAULT_MAX_DEPTH)
parser.add_argument('-t', '--timeout', help='Timeout in seconds', required=False, default=CRAWLX_DEFAULT_TIMEOUT)
parser.add_argument('-l', '--log', help='Log file', required=False, default='crawlx.log')
parser.add_argument('-j', '--json', help='JSON output file', required=False, default='crawlx.json')
parser.add_argument('-v', '--verbose', help='Verbose output', required=False, action='store_true')
parser.add_argument('-q', '--quiet', help='Quiet output', required=False, action='store_true')
parser.add_argument('--delay', help='Delay between requests', required=False, default=0)
args = parser.parse_args()

# Initialize the session with a FuturesSession
session = FuturesSession()
found_links = []
first_crawl = []
second_crawl = []
third_crawl = []

# (First Crawl) Crawl the home page using the session
print("Crawling " + args.url)
first_crawl += crawl(url=args.url, depth=int(args.depth), timeout=int(args.timeout))

# (Second Crawl) Crawl the links in the first_crawl using the session
print("(Crawl 2) Crawling " + str(len(first_crawl)) + " links")
for link in first_crawl:
    second_crawl += crawl(url=link, depth=int(args.depth), timeout=int(args.timeout))

# (Third Crawl) Crawl the links in the second_crawl using the session
print("(Crawl 3) Crawling " + str(len(second_crawl)) + " links")
for link in second_crawl:
    third_crawl += crawl(url=link, depth=int(args.depth), timeout=int(args.timeout))


# Display Output
found_links = first_crawl + second_crawl + third_crawl
found_links = list(set(found_links))
print("Found " + str(len(found_links)) + " total unique links")
print(found_links)
