# requests to get url, os to interact with dirs,
# bs4 and urllib to
# parse html and urls.
import requests, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

#validator
def validateurl(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#Get all urls internal and external.
def get_all_website_links(url):
    #minit set of urls
    urls = set()
    # strip frills off url and apply bs4 for parsing
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    #find all href links
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        #skip empty tags
        if href == "" or href is None:
            continue
        #make all links absolute
        href = urljoin(url,href)
        parsed_href = urlparse(href)
        #make sure urls are double extra clean.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        #skip bad links
        if not validateurl(href):
            continue
        #add external urls to external link set
        if domain_name not in href:
            if href not in external_urls:
                external_urls.add(href)
            continue
        #add all urls to url and internal urls to internal set
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawler(url, max_urls):
    #init counter and count.
    global total_urls_visited

    total_urls_visited += 1

    links = get_all_website_links(url)

    #recursive crawl
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawler(link, max_urls=max_urls)

#get url from user or choose default url (my website)
url = input("input url (https://example.com): ")

max_urls = int(input("Set maximum links web_backup will follow: "))

dir_name = input("Name the output file that will be created: ")

#create and populate sets of urls on website init counter
total_urls_visited = 0
internal_urls = set()
external_urls = set()
crawler(url,max_urls)
