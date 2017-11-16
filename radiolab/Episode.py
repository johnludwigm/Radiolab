
import requests
from bs4 import BeautifulSoup

import re
downloadreg = re.compile(r"(https://www\.podtrac\.com/pts/redirect\.mp3/audio\.wnyc\.org/[/_\w\d]+.mp3)")

#There was a weird problem with filenames - some filenames randomly saved as "?     <episode-name>.mp3"
def downloadmp3(filename, sourceurl):
  """Saves mp3 file from url to file `filename`."""
  
  with open("%s.mp3" % filename.replace("?", "").strip(), "wb") as fileobj:
    fileobj.write(requests.get(sourceurl).content)

class Episode:
  """Main class to handle Radiolab episodes when user is downloading directly through http://www.radiolab.org/archive"""

  def __init__(self, soup):
    self.soup = soup
    self.title = ''
    self.downloadurl = ''
    self.date = (self.soup).find("h3", {"class": "date"}).get_text().strip()

  def gettitle(self):
    """Sets title for Episode object."""
    
    parent = (self.soup).find("h2", {"class": "title"})
    self.title = parent.find("a").get_text().strip()

  def getdownloadurl(self):
    """Returns download url for the episode's mp3 file."""
    
    result = downloadreg.search((self.soup).get_text())
    try:
      self.downloadurl = result.groups()[0]
    except Exception as exc:
      print("Episode %s has exception: %s" % (self.title, exc))

  def download(self):
    """Downloads episode."""
    
    downloadmp3(self.downloadurl, self.title)

  def formatinfo(self):
    """Generates episode info for the page https://github.com/johnludwigm/Radiolab/blob/master/info.txt"""
    
    return "Title:\t%s\nDate:\t%s\nURL:\t%s\n\n" % (self.title, self.date, self.downloadurl)

  def markdowninfo(self):
    """Generates episode info in markdown for the page https://github.com/johnludwigm/Radiolab/blob/master/Episodes.md"""
    
    return "**[%s](%s)**\n\n%sn\n---\n\n" % (self.title, self.date, self.downloadurl)
