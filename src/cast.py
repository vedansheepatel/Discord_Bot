import requests
from bs4 import BeautifulSoup

def get_cast(drama_url):
    response = requests.get(drama_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    cast=[]

    mainbox = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find('div', class_='box clear')
    casts = mainbox.find_all("li", class_="list-item col-sm-4")
   
    def get_poster(link):
        response = requests.get('https://mydramalist.com'+link)
        soup = BeautifulSoup(response.content, 'html.parser')
        poster=soup.find("div", class_="col-lg-8 col-md-8").find("img", class_="img-responsive inline")['src']

        return poster
    
    for item in casts:
        name = item.find("a", class_="text-primary text-ellipsis")['title']
        role= item.find('div', class_='text-ellipsis').text
        type= item.find("small", class_="text-muted").text
        link = item.find('div', class_='col-xs-4 col-sm-5 p-r p-l-0 credits-left').find('a')['href']
        
        cast.append(
            {
                "Name": name,
                "Role": role,
                "Type": type,
                "Poster": get_poster(link)
                
            }
        )
    
    return cast