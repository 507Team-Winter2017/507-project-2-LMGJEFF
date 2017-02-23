#proj2.py
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

### Your Problem 1 solution goes here
html = urlopen("http://nytimes.com").read()
soup = BeautifulSoup(html, "html.parser")
for story_heading in soup.find_all(class_="story-heading", limit=10):
    if story_heading.a:
        print(story_heading.a.text.replace("\n", " ").strip())
    else:
        print(story_heading.contents[0].strip())

#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Problem 2 solution goes here
html = urlopen("https://www.michigandaily.com/").read()
soup = BeautifulSoup(html, "html.parser")
for most_read in soup.find_all(class_="panel-pane pane-mostread"):
    for li in most_read.find_all('li'):
        if li.a:
            print(li.a.text.replace("\n", " ").strip())
        else:
            print(li.contents[0].strip())

#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

### Your Problem 3 solution goes here
html = urlopen("http://newmantaylor.com/gallery.html").read()
soup = BeautifulSoup(html, "html.parser")
for img in soup.find_all('img'):
    print(img.get('alt', 'No alternative text provided!'))

#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

### Your Problem 4 solution goes here
site = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4"
req = Request(site, None, {'User-Agent': 'SI_CLASS'})
html = urlopen(req).read()
soup = BeautifulSoup(html, "html.parser")
i = 1
while True:
    for a in soup.find_all('a', text="Contact Details"):
        site_iter = urljoin(site, a.get('href'))
        req_iter = Request(site_iter, None, {'User-Agent': 'SI_CLASS'})
        html_iter = urlopen(req_iter).read()
        soup_iter = BeautifulSoup(html_iter, "html.parser")
        for div1 in soup_iter.find_all('div', class_=re.compile('person-email')):
            for div2 in div1.find_all('div', class_="field-item even"):
                print(i, div2.a.text.replace("\n", " ").strip())
                i += 1
    find = soup.find('a', title="Go to next page")
    if not find:
        break
    site_next = urljoin(site, find.get('href'))
    req_next = Request(site_next, None, {'User-Agent': 'SI_CLASS'})
    html_next = urlopen(req_next).read()
    soup = BeautifulSoup(html_next, "html.parser")