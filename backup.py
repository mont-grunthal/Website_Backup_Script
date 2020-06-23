import requests, os
from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urlparse, urljoin
from pathlib import Path

import web_crawler as wc


#get url sets and dirname from crawler.
internal_urls = wc.internal_urls
external_urls = wc.external_urls
dir_name = wc.dir_name
url = wc.url


#current date for recordkeeping
today = date.today()
date = today.strftime("%d/%m/%Y")
#make parent and leaf dirs.
os.makedirs(dir_name+"/info",exist_ok = True)
os.makedirs(dir_name+"/html",exist_ok = True)
os.makedirs(dir_name+"/media",exist_ok = True)

#populate info folder with website, backup date, and links.
f = open(dir_name + "/info/info.txt", "w+")
f.write(f"Website Name: {url} \n")
#TODO get time
f.write(f"Backup date: {date} \n")
f.write("Internal Links: \n")
for link in internal_urls:
    f.write(f"{link} \n" )
f.write("External Links: \n")
for link in external_urls:
    f.write(f"{link} \n" )
f.close()



#populate html folder with each pages html.
for i,link in enumerate(internal_urls):
    #download page
    parts = link.split('/');
    lastsegment = parts[-1];
    soup = BeautifulSoup(requests.get(link).content, "html.parser")
    #creat .txt file for that page and names it
    cur_dir = str(dir_name) + f"/html/{lastsegment}.html"
    f = open(cur_dir, "w+")
    f.write(f"Internal link number: {i} \n")
    out = soup.prettify()
    f.write(out)



#for i,link in enumerate(internal_urls):
#    #download page
#    lastsegment = parts[-1];
#    soup = BeautifulSoup(requests.get(link).content, "html.parser")
#    cur_dir = str(dir_name) + f"/media/{lastsegment}.html"
#    f = open(cur_dir, "w+")
#    f.write(f"Internal link number: {i} \n")
#    out = soup.prettify()
#    f.write(out)
