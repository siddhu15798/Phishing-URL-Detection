from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse, urlencode
from urllib.error import HTTPError

url = 'http://www.reo15.moe.go.th'


def Links_pointing_to_page(url):
    
    count = 0
    try:
        r = urllib.request.urlopen(url)
        soup = BeautifulSoup(r, "html.parser")
        for link in soup.find_all('a'):
            #print(link.get('href'))
            count += 1
    except TypeError:
        return 1
    except HTTPError:
        return 2
    
    if(count == 0):
        return 1 #phishing
    elif(count == 1):
        return 2 #suspicious
    else:
        return 0 #legitimate
    
a = Links_pointing_to_page(url)
print(a)