
import requests
from bs4 import BeautifulSoup

class PageOfEpisodes:
  """Class to parse pages in the Radiolab archive and get episodes."""

  def __init__(self, url):
    
    reqobj = requests.get(url)
    self.url = url
    self.contents = ''
    try:
      self.soup = BeautifulSoup(reqobj.text, "html.parser")
    except Exception as exc:
      print("PageOfEpisodes-Exception occurred during initialization:\n\t%s" % exc)

  def getepisodes(self):
    """Returns list of episodes on the page in chronological order."""
    
    #Reversed because a page has the newest episodes at the top and oldest at the bottom.
    self.contents = reversed((self.soup).find_all("div", {"class": "series-item"}))
