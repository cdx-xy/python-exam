import urllib.request
from html.parser import HTMLParser

def open_url(url):
  req = urllib.request.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')
  response = urllib.request.urlopen(req)
  html = response.read().decode('utf-8')
  return html

url = 'https://www.baidu.com/s?wd=%E5%85%B3%E6%97%AD&rsv_spt=1&rsv_iqid=0xd90a906900058af8&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=8&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=1566&rsv_sug4=1776&rsv_sug=1'
html = open_url(url)
# print(html)

# file = open('baidu.html', 'w', encoding='utf-8')
# file.write(html)
# file.close()

inH3 = False
inA = False
inEm = False
currentTitle = ''
currentLink = ''
index = 1


class MyHTMLParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    global inH3
    global inA
    global inEm
    global currentLink

    if 'h3' == tag:
      inH3 = True
    else:
      if 'a' == tag and inH3 :
        for attr in attrs:
          if attr[0] == 'href':
            currentLink = attr[1]

        inA = True
      else:
        if 'em' == tag and (inA or inEm):
          inEm = True
        else:
          inEm = False
        inA = False
      inH3 = False

  def handle_endtag(self, tag):
    global inA
    global currentTitle
    global currentLink
    global index
    if (inA or inEm) and tag == 'a':
      print('-------- ' + str(index) + ' --------')
      print('标题: ' + currentTitle)
      print('链接: ' + currentLink)
      currentTitle = ''
      index = index + 1

  def handle_data(self, data):
    global inH3
    global inA
    global inEm
    global currentTitle

    if inA or inEm:
      text = data.strip()
      if text != '':
        currentTitle = currentTitle + text

parser = MyHTMLParser()

print('关于“曹殿雪”的百度搜索结果第一页')
parser.feed(html)
