import requests
from bs4 import BeautifulSoup


sqm = -1

r = requests.get('http://astro.physics.umanitoba.ca/sqm/') 
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('div', id='data')
content = s.find_all('pre') 

if content != []:
    
    content = str(content).split("\n")
    last = content[-2].split(",")
    sqm = last[1].strip()
    sqm = sqm[:-1]



def get_sqm() -> float:
    return sqm