import requests
from bs4 import BeautifulSoup

def get_recs(drama_url):
    response = requests.get(drama_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rec_list=[]
    
    image = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find("img", class_="img-responsive")['src']
    mainbox = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find('div', class_='box-body details-recommendations')
    rec_list.append(image)
    
    detailed_info = mainbox.find("div", class_="row p-l-sm p-r-sm").find_all("div", class_="rec-item col-xs-4 col-md-2 p-a-xs")
    for item in detailed_info:
        rec_list.append((item.find('a')['title']))
    return rec_list
