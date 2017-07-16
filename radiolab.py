  
import os
import re
import requests
from bs4 import BeautifulSoup

regex = re.compile(r"(https://www\.podtrac\.com/pts/redirect\.mp3/audio\.wnyc\.org/[/_a-zA-z0-9]+.mp3)")

def createdir(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)

class Episode:

  def __init__(self, soupitem):
    self.soup = soupitem
    self.title = ''
    self.downloadurl = ''
    self.date = (self.soup).find("h3", {"class": "date"}).get_text()

  def gettitle(self):
    parent = (self.soup).find("h2", {"class": "title"})
    self.title = parent.find("a").get_text()

  def download(self):
    downloadreg = regex.search((self.soup).get_text())
    try:
      downloadurl = downloadreg.groups()[0]
      #there's a weird problem with with filenames
      with open("{}.mp3".format(self.title.replace("?", "").strip()), "wb") as fileobj:
        fileobj.write(requests.get(downloadurl).content)
    except:
      pass
    
class PageofEpisodes:

  def __init__(self, url):
    reqobj = requests.get(url)
    self.contents = ''
    try:
      self.soup = BeautifulSoup(reqobj.text, "html.parser")
    except Exception as exc:
      print("Exception occurred during initialization:\n\t{}".format(exc))

  def getepisodes(self):
    self.contents = (self.soup).find_all("div", {"class": "series-item"})

parentdir = ''

def main(downloadfolder):
  reqobj = requests.get(r"http://www.radiolab.org/series/podcasts/9999999")

  os.chdir(parentdir)
  createdir(downloadfolder); os.chdir(downloadfolder)

  currentsoup = BeautifulSoup(reqobj.text, "html.parser")
  current = int(currentsoup.find("span", {"class", "pagefooter-current"}).get_text().strip())

  while current > 0:
    page = PageofEpisodes("http://www.radiolab.org/series/podcasts/{}/".format(current))
    page.getepisodes()
    for item in page.contents:
      episode = Episode(item)
      episode.gettitle()
      episode.download()
    current -= 1
