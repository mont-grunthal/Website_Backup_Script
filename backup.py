import requests, os
from bs4 import BeautifulSoup
from datetime import date
from urllib.parse import urlparse, urljoin
import web_crawler as wc


#get url sets and dirname from crawler.
internal_urls = wc.internal_urls
external_urls = wc.external_urls
dir_name = wc.dir_name
url = wc.url

#make parent and leaf dirs.
os.makedirs(dir_name+"/info",exist_ok = True)
os.makedirs(dir_name+"/html",exist_ok = True)
os.makedirs(dir_name+"/media",exist_ok = True)


#domain and date for recordkeeping in info.
domain = urlparse(url).netloc
today = date.today()
date = today.strftime("%d/%m/%Y")

#populate info folder with website, backup date, and links.
f = open(dir_name + "/info/info.txt", "w+")
f.write(f"Website Name: {domain} \n")
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
for link in internal_urls:
    #download page
    parts = link.split('/');
    lastsegment = parts[-1];
    soup = BeautifulSoup(requests.get(link).content, "html.parser")

    #html#

    #creates .txt file for that pages html
    cur_dir_html = str(dir_name) + f"/html/{lastsegment}.html"
    f_html = open(cur_dir_html, "w+")
    #populate with pages html content.
    html_out = soup.prettify()
    f_html.write(html_out)
    f_html.close()

    #media#

    for img in soup.findAll(['img','image', 'iframe']):
        os.makedirs(dir_name+f"/media/{lastsegment}",exist_ok = True)
        #create file for that pages media
        imgurl = url + img.get('src')
        res = requests.get(imgurl)
        parts = imgurl.split('/');
        lastsegimg = parts[-1];
        cur_dir_media = str(dir_name) + f"/media/{lastsegment}/{lastsegimg}"
        f_media = open(cur_dir_media, "wb+")
        for chunk in res.iter_content(100000):
            f_media.write(chunk)
