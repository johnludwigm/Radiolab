

import os
import re
import requests
from bs4 import BeautifulSoup
from sys import argv
from .Episode import Episode, downloadmp3
from .PageOfEpisodes import PageOfEpisodes

github_url = "https://raw.githubusercontent.com/johnludwigm/Radiolab/master/Radiolab_Episodes.txt"

import argparse
def parse(args):
  parser = argparse.ArgumentParser()
  parser.add_argument('-dl', '--download', nargs='*', default = '')
  parser.add_argument('-dest', '--destination', nargs='?', default='~')
  parser.add_argument('-dlall', '--downloadall')
  return vars(parser.parse_args(args[1:]))

def radiolabpages(lastpage = 9999999):
  reqobj = requests.get("http://www.radiolab.org/series/podcasts/%s" % lastpage)
  currentsoup = BeautifulSoup(reqobj.text, "html.parser")

  #current is the current page number
  current = int(currentsoup.find("span", {"class", "pagefooter-current"}).get_text().strip())
  while current > 0:
    if current != 1:
      yield PageOfEpisodes("http://www.radiolab.org/series/podcasts/%s/" % current)
    else:
      yield PageOfEpisodes("http://www.radiolab.org/series/podcasts/")
    current -= 1

#Instead of running through all available pages in the Radiolab archives
#to get the episodes and their links, the package by default will get the episodes
#from a JSON file on my GitHub page.
def fromgithub():
  res = requests.get(github_url)

  #transform res.content into a Python dictionary
  return eval(res.content)  

def downloadall():
  for episode, episode_url in fromgithub().items():
    try:
      downloadmp3(episode, episode_url)
    except Exception as exc:
      print("Unable to download %s:\n%s\n," % (episode, exc))

def generatejson(outputfilename):
  from collections import OrderedDict
  from json import dumps

  episode_to_url = {}
  for page in radiolabpages():
    print(page.url)
    page.getepisodes()
    for item in page.contents:
      episode = Episode(item)
      episode.gettitle(); episode.getdownloadurl()
      episode_to_url[episode.title] = episode.downloadurl

  jsondict = OrderedDict(sorted(episode_to_url.items(), key = lambda a: a[0]))
  with open(outputfilename, "w", encoding = "utf-8") as fileobj:
    fileobj.write(dumps(jsondict, indent = "\t"))

def generatemd(outputfilename):
  if not outputfilename.endswith(".md"):
    outputfilename = outputfilename + ".md"

  with open(outputfilename, "w", encoding = "utf-8") as fileobj:
    for page in radiolabpages():
      page.getepisodes()
      for episode in page.contents:
        fileobj.write(episode.markdowninfo())

def main(args = None):
  if args is None:
    args = argv
  
  if len(args) == 1:
    print("Please refer to https://github.com/johnludwigm/Radiolab/blob/master/README.md for examples of proper usage.")
    return
  
  cli = parse(argv)
  if "destination" in cli:
    try:
      os.chdir(cli["destination"])
    except Exception as exc:
      print("Unable to change directories:\n%s" % exc)
  if cli["downloadall"]:
    downloadall()
  elif "download" in cli:
    episode_to_url = fromgithub()
    for episode in cli["download"]:
      downloadmp3(episode, episode_to_url[episode])
    
if __name__ == "__main__":
  main()



