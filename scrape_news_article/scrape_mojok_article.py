from bs4 import BeautifulSoup
import requests

class Content:
  # Menginisialisasi url, title, dan body
  def __init__(self, url, title, body):
    self.url = url
    self.title = title
    self.body = body

# Mengambil text dari url yang ditentukan
def getPage(url):
  req = requests.get(url)
  return BeautifulSoup(req.text, 'html.parser')

def scrapeMojok(url):
  bs = getPage(url)
  title = bs.find('h1').text
  # Menentukan struktur html yang dipilih untuk mengscrape artikel yang ditentukan.
  lines = bs.select('div.content-inner p')
  body = '\n'.join([line.text for line in lines])
  return Content(url, title, body)

# Memberikan nilai pada url dimana letak artikel yang akan di scrape
url = 'https://mojok.co/pojokan/saya-nikah-muda-dan-saya-baik-baik-saja/'
content = scrapeMojok(url)
print('Title: {}'.format(content.title))
print('URL: {}'.format(content.url))
print(content.body)
