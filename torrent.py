from urllib.parse import quote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import subprocess


class Torrent:
    def __str__(self):
        return "(%s / %s) (%s) (%s) (%d SE / %d LE) %s" % (self.category,
                                                           self.subcategory,
                                                           self.size,
                                                       self.date,
                                                           self.seeders,
                                                           self.leeches,
                                                           self.name)

    def transmission_client(self, client):
        self.client = client

    def download(self):
        print("dis da magnet link")
        #webbrowser.open(self.magnet, autoraise=False)
        print(self.magnet)
        subprocess.call("sh transmission.sh %s" % (self.magnet), shell=True)

    def add_inner_url(self,url,inner):
        self.inner_url = str(url)+str(inner)

    def add_magnet(self,magnet):
        self.magnet = magnet

def search_engine(torrent_name):

    #first search to find a suitable torrent
    torrents = search(torrent_name)

    # only for BlueRay quality
    for torrent in torrents:
        if "1080p" not in torrent.__str__():
           torrents.remove(torrent)

    for torrent in torrents:
        print(torrent.__str__())

    #choose a torrent and download it
    torrent = torrents[0]
    download_torrent(torrent,torrent.inner_url)






def search(keywords):

    domain = "http://proxtpb.art"
    url = '%s/search/%s/0/' % (domain, quote(keywords))

    print("url")
    print(url)
    return parse_pirate(domain,url)

def parse_pirate(domain,url):

    META_REGEX_FORMAT = "Uploaded (.*), Size (.*), ULed by (.*)"
    UNICODE_BLANK = '\xa0'
    BLANK = ' '
    ROWS = 'tr'
    DATA = 'td'

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)

    torrents = []
    for result in soup.find_all(ROWS)[1:]:
        torrent = Torrent()
        data = result.find_all(DATA)

        a = data[0].find_all('a')
        torrent.category = a[0].string
        torrent.subcategory = a[1].string

        a = data[1].find_all('a')
        torrent.link = a[0]['href']
        torrent.name = a[0].string
        torrent.magnet = a[1]['href']

        torrent.user = data[1].font.a
        if torrent.user is not None:
            torrent.user = torrent.user.text
        else:
            torrent.user = data[1].font.i.text

        pattern = re.compile(META_REGEX_FORMAT)
        match = pattern.match(data[1].font.text)

        torrent.date = match.group(1).replace(UNICODE_BLANK, BLANK)
        torrent.size = match.group(2).replace(UNICODE_BLANK, BLANK)

        torrent.seeders = int(data[2].text)
        torrent.leeches = int(data[3].text)

        torrent.add_inner_url(domain,torrent.magnet)
        #print("inner url")
        #print(torrent.inner_url)

        torrents.append(torrent)
    return torrents


def download_torrent(torrent,url):

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)

    print(soup)


    #d = soup.find_all("div", {"class": "download"})

    #print (d)

    magnet_link= [div.a for div in
                    soup.findAll('div', attrs={'class': 'download'})]

    torrent.add_magnet(magnet_link[0]['href'])
    torrent.download()



