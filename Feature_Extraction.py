import re
import time
import whois
import socket
import requests
import pandas as pd
import urllib.request
from google import search
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.parse import urlparse, urlencode
from urllib3.exceptions import NewConnectionError


url = input("Enter the URL you want to check: ")
#Raw_Data = pd.read_csv("Legitimate-URLS.csv", header=None, names=['urls'])

Protocol = []
Domain = []
Path = []
Length_URL = []
Having_At_Symbol = []
Redirection_Symbol = []
Prefix_Suffix_Separation = []
Sub_Domains = []
Having_IP = []
Tiny_URL = []
Http_Tokens = []
Web_Traffic = []
Domain_Registration_Length = []
Age_Of_Domain = []
Dns_Record = []
Statistical_Report = []
Email_Submit = []
Links_In_Tags = []

class Feature_Extraction:
    
    # 1 - Phishing
    #-1 - Legitimate
    # 0 - Suspicious
    
    def __init__(self):
        pass
    
    def Get_Protocol(self, url):
        return urlparse(url).scheme
    
    def Get_Domain(self, url):
        return urlparse(url).netloc
    
    def Get_Path(self, url):
        return urlparse(url).path

    def Long_URL(self, url):
        if len(url) < 54:
            return -1
        elif len(url) >= 54 and len(url) <= 75:
            return 0
        else:
            return 1
        
    def Have_Symbol_Attherate(self, url):
        if "@" in url:
            return 1
        else: 
            return -1
        
    def Redirection(self, url):
        if "//" in urlparse(url).path:
            return 1
        else:
            return -1
        
    def Prefix_Suffix_Separation(self, url):
        if '-' in urlparse(url).netloc:
            return 1
        else:
            return -1
        
    def Sub_Domains(self, url):
        if url.count(".") < 3:
            return -1        
        elif url.count(".") == 3:
            return 0       
        else:
            return 1        
        
    def Ip_Address(self, url):
        match = re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  #IPv4
                        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  #IPv4 in hexadecimal
                        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)
        if match:
            return 1
        else:
            return -1
        
    def Shortening_Service(self, url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                        'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                        'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                        'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                        'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                        'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                        'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',url)
        if match:
            return 1
        else:
            return -1

    def Https_Token(self, url):
        match = re.search('https://|http://',url)
        try:
            if match.start(0)==0 and match.start(0) is not None:
                url = url[match.end(0):]
                match = re.search('http|https',url)
                if match:
                    return 1
                else:
                    return -1
        except:
            return 1
        
    def Web_Traffic(self, url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        except TypeError:
            return 1
        except HTTPError:
            return 2
        rank = int(rank)
        if (rank<100000):
            return 0
        else:
            return 2
        
    def Domain_Reg_Length(self, url):
        dns = 0
        try:
            domain_name = whois.whois(urlparse(url).netloc)
        except:
            dns = 1
        
        if dns == 1:
            return 1      #phishing
        else:
            expiration_date = domain_name.expiration_date
            today = time.strftime('%Y-%m-%d')
            today = datetime.strptime(today, '%Y-%m-%d')
            if expiration_date is None:
                return 1
            elif type(expiration_date) is list or type(today) is list :
                return 2     #If it is a type of list then we can't select a single value from list. So,it is regarded as suspected website  
            else:
                creation_date = domain_name.creation_date
                expiration_date = domain_name.expiration_date
                if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
                    try:
                        creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                        expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
                    except:
                        return 2
                registration_length = abs((expiration_date - today).days)
                if registration_length / 365 <= 1:
                    return 1 #phishing
                else:
                    return 0 # legitimate
        
    def Age_Of_Domain(self, url):
        dns = 0
        try:
            domain_name = whois.whois(urlparse(url).netloc)
        except:
            dns = 1
        
        if dns == 1:
            return 1
        else:
            creation_date = domain_name.creation_date
            expiration_date = domain_name.expiration_date
            if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
                try:
                    creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
                    expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
                except:
                    return 2
            if ((expiration_date is None) or (creation_date is None)):
                return 1
            elif ((type(expiration_date) is list) or (type(creation_date) is list)):
                return 2
            else:
                ageofdomain = abs((expiration_date - creation_date).days)
                if ((ageofdomain/30) < 6):
                    return 1
                else:
                    return 0
        
    def Dns_Record(self, url):
        dns = 0
        try:
            domain_name = whois.whois(urlparse(url).netloc)
            print(domain_name)
        except:
            dns = 1
            
        if dns == 1:
            return 1
        else:
            return dns
        
    def Statistical_Report(self, url):
        hostname = url
        h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
        z = int(len(h))
        if z != 0:
            y = h[0][1]
            hostname = hostname[y:]
            h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
            z = int(len(h))
            if z != 0:
                hostname = hostname[:h[0][0]]
        url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
        try:
            ip_address = socket.gethostbyname(hostname)
            ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)  
        except:
            return 1

        if url_match:
            return 1
        else:
            return 0
        
    def Email_Submit(self, url):
        try:
            opener = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(opener, 'lxml')
            if(soup.find('mailto:')):
                return 1
            else:
                return 0
        except:
            return 2
        
    def Links_In_Tags(self, url):
        try:
            opener = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(opener, 'lxml')  
            no_of_meta =0
            no_of_link =0
            no_of_script =0
            anchors=0
            avg =0
            
            for meta in soup.find_all('meta'):
                no_of_meta = no_of_meta+1
            for link in soup.find_all('link'):
                no_of_link = no_of_link +1
            for script in soup.find_all('script'):
                no_of_script = no_of_script+1
            for anchor in soup.find_all('a'):
                anchors = anchors+1
            total = no_of_meta + no_of_link + no_of_script+anchors
            tags = no_of_meta + no_of_link + no_of_script
            
            if(total!=0):
                avg = tags/total
            if(avg<0.25):
                return 0
            elif(0.25<=avg<=0.81):
                return 2
            else:
                return 1        
        except:        
            return 2
        
    def favicon(self, wiki, soup, domain):
        for head in soup.find_all('head'):
            for head.link in soup.find_all('link', href=True):
                dots = [x.start() for x in re.finditer(r'\.', head.link['href'])]
                return 1 if wiki in head.link['href'] or len(dots) == 1 or domain in head.link['href'] else -1
        return 1
    
    def url_of_anchor(wiki, soup, domain):
        i = 0
        unsafe = 0
        for a in soup.find_all('a', href=True):
            # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and ::
            # might not be
            # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                    wiki in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1
            # print a['href']
        try:
            percentage = unsafe / float(i) * 100
        except:
            return 1
        if percentage < 31.0:
            return 1
            # return percentage
        elif 31.0 <= percentage < 67.0:
            return 0
        else:
            return -1
        
    def request_url(wiki, soup, domain):
        i = 0
        success = 0
        for img in soup.find_all('img', src=True):
            dots = [x.start() for x in re.finditer(r'\.', img['src'])]
            if wiki in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start() for x in re.finditer(r'\.', audio['src'])]
            if wiki in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start() for x in re.finditer(r'\.', embed['src'])]
            if wiki in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for i_frame in soup.find_all('i_frame', src=True):
            dots = [x.start() for x in re.finditer(r'\.', i_frame['src'])]
            if wiki in i_frame['src'] or domain in i_frame['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        try:
            percentage = success / float(i) * 100
        except:
            return 1

        if percentage < 22.0:
            return -1
        elif 22.0 <= percentage < 61.0:
            return 0
        else:
            return 1
        
    def links_in_tags(wiki, soup, domain):
        i = 0
        success = 0
        for link in soup.find_all('link', href=True):
            dots = [x.start() for x in re.finditer(r'\.', link['href'])]
            if wiki in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i + 1

        for script in soup.find_all('script', src=True):
            dots = [x.start() for x in re.finditer(r'\.', script['src'])]
            if wiki in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i + 1
        try:
            percentage = success / float(i) * 100
        except:
            return 1

        if percentage < 17.0:
            return 1
        elif 17.0 <= percentage < 81.0:
            return 0
        else:
            return -1

    def sfh(wiki, soup, domain):
        for form in soup.find_all('form', action=True):
            if form['action'] == "" or form['action'] == "about:blank":
                return -1
            elif wiki not in form['action'] and domain not in form['action']:
                return 0
            else:
                return 1
        return 1
    
    def i_frame(soup):
        
        for i_frame in soup.find_all('i_frame', width=True, height=True, frameBorder=True):
        # Even if one iFrame satisfies the below conditions, it is safe to return -1 for this method.
            if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameBorder'] == "0":
                return -1
            if i_frame['width'] == "0" or i_frame['height'] == "0" or i_frame['frameBorder'] == "0":
                return 0
        # If none of the iframes have a width or height of zero or a frameBorder of size 0, then it is safe to return 1.
        return 1
    
    def google_index(self, url):
        site = search(url, 5)
        return 1 if site else -1
    
    def Links_pointing_to_page(self, url):
        
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
        
fe = Feature_Extraction()
# rows = len(Raw_Data["urls"])

# for i in range(0, rows):
    # url = Raw_Data["urls"][i]
    
Protocol.append(fe.Get_Protocol(url))
Domain.append(fe.Get_Domain(url))
Path.append(fe.Get_Path(url))
Length_URL.append(fe.Long_URL(url))
Having_At_Symbol.append(fe.Have_Symbol_Attherate(url))
Redirection_Symbol.append(fe.Redirection(url))
Prefix_Suffix_Separation.append(fe.Prefix_Suffix_Separation(url))
Sub_Domains.append(fe.Sub_Domains(url))
Having_IP.append(fe.Ip_Address(url))
Tiny_URL.append(fe.Shortening_Service(url))
Http_Tokens.append(fe.Https_Token(url))
Web_Traffic.append(fe.Web_Traffic(url))
Domain_Registration_Length.append(fe.Domain_Reg_Length(url))
Age_Of_Domain.append(fe.Age_Of_Domain(url))
Dns_Record.append(fe.Dns_Record(url))
Statistical_Report.append(fe.Statistical_Report(url))
Email_Submit.append(fe.Email_Submit(url))
Links_In_Tags.append(fe.Links_In_Tags(url))
    
print(Protocol)
print(Domain)
print(Path)
print(Length_URL)
print(Having_At_Symbol)
print(Redirection_Symbol)
print(Prefix_Suffix_Separation)
print(Sub_Domains)
print(Having_IP)
print(Tiny_URL)
print(Http_Tokens)
print(Web_Traffic)
print(Domain_Registration_Length)
print(Age_Of_Domain)
print(Dns_Record)
print(Statistical_Report)
print(Email_Submit)
print(Links_In_Tags)

# Label = []
# for i in range(0, rows):
#     Label.append(1)
    
d = {'Protocol':pd.Series(Protocol),'Domain':pd.Series(Domain),'Path':pd.Series(Path),'Having_IP':pd.Series(Having_IP),
    'Length_URL':pd.Series(Length_URL),'Having_@_Symbol':pd.Series(Having_At_Symbol),
    'Redirection_Symbol':pd.Series(Redirection_Symbol),'Prefix_Suffix_Separation':pd.Series(Prefix_Suffix_Separation),
    'Sub_Domains':pd.Series(Sub_Domains),'Tiny_URL':pd.Series(Tiny_URL),'Web_Traffic' : pd.Series(Web_Traffic) ,
    'Domain_Registration_Length':pd.Series(Domain_Registration_Length),'Dns_Record':pd.Series(Dns_Record),
    'Statistical_Report':pd.Series(Statistical_Report),'Age_Of_Domain':pd.Series(Age_Of_Domain),'Http_Tokens':pd.Series(Http_Tokens),
    'Email_Submit':pd.Series(Email_Submit),'Links_In_Tags':pd.Series(Links_In_Tags)}#,'Label':pd.Series(Label)}

data = pd.DataFrame(d)
data.to_csv("a.csv", index=False, encoding='UTF-8')
