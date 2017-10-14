
import requests
from bs4 import BeautifulSoup

import re
downloadreg = re.compile(r"(https://www\.podtrac\.com/pts/redirect\.mp3/audio\.wnyc\.org/[/_\w\d]+.mp3)")

#There was a weird problem with with filenames: Some saved as "? 
def downloadmp3(filename, sourceurl):
  with open("%s.mp3" % filename.replace("?", "").strip(), "wb") as fileobj:
    fileobj.write(requests.get(sourceurl).content)

class Episode:

  def __init__(self, soup):
    self.soup = soup
    self.title = ''
    self.downloadurl = ''
    self.date = (self.soup).find("h3", {"class": "date"}).get_text().strip()

  def gettitle(self):
    parent = (self.soup).find("h2", {"class": "title"})
    self.title = parent.find("a").get_text().strip()

  def getdownloadurl(self):
    result = downloadreg.search((self.soup).get_text())
    try:
      self.downloadurl = result.groups()[0]
    except:
      pass

  def download(self):
    downloadmp3(self.downloadurl, self.title)

  def formatinfo(self):
    return "Title:\t%s\nDate:\t%s\nURL:\t%s\n\n" % (self.title, self.date, self.downloadurl)

  def markdowninfo(self):
    return "**[%s](%s)**\n\n%sn\n---\n\n" % (self.title, self.date, self.downloadurl)
