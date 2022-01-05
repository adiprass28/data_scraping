class Website:

  def __init__(self, name, url, targetPattern, absoluteUrl, titleTag, bodyTag):
    self.name = name
    self.url = url
    self.targetPattern = targetPattern
    self.absoluteUrl = absoluteUrl
    self.titleTag = titleTag
    self.bodyTag = bodyTag

class Content:

  def __init__(self, url, title, body):
    self.url = url
    self.title = title
    self.body = body

  def print(self):
    print("URL: {}".format(self.url))
    print("Title: {}".format(self.title))
    print("BODY: {}".format(self.body))

from bs4 import BeautifulSoup
import requests
import re

class Crawler:
  def __init__(self, site):
    self.site = site
    self.visited = []

  def getPage(self, url):
    try:
      req = requests.get(url)
    except requests.exceptions.RequestException:
      return None
    return BeautifulSoup(req.text, 'html.parser')

  def safeGet(self, pageObj, selector):
    selectedElems = pageObj.select(selector)
    if selectedElems is not None and len(selectedElems) > 0:
      return '\n'.join([elem.get_text() for elem in selectedElems])
    return ''

  def parse(self, url):
    bs = self.getPage(url)
    if bs is not None:
      title = self.safeGet(bs, self.site.titleTag)
      body = self.safeGet(bs, self.site.bodyTag)
      if title != '' and body != '':
        content = Content(url, title, body)
        content.print()

  def crawl(self):
    """
    Mengambil halaman dari halaman utama website
    """
    bs = self.getPage(self.site.url)
    # Menemukan url mana yang akan discraping mengguakan regex
    targetPages = bs.findAll('a', href=re.compile(self.site.targetPattern))
    for targetPage in targetPages:
      # menargetkan atribut 'href'
      targetPage = targetPage.attrs['href']
      if targetPage not in self.visited:
        self.visited.append(targetPage)
        if not self.site.absoluteUrl:
          targetPage = '{}{}'.format(self.site.url, targetPage)
        self.parse(targetPage)

reuters = Website('Mojok', 'http://www.mojok.co', '(/liputan/)',
                  True, 'h1', 'div.content-inner')
crawler = Crawler(reuters)
crawler.crawl()