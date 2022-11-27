import requests
from bs4 import BeautifulSoup

def get_rankings():
    rankings= []
    titles = []
    info = []
    page1={}
    page2={}
    page3={}
    page4={}
    page5={}
    
    i=1
    while i<6:
        response = requests.get('https://mydramalist.com/shows/top?page='+str(i))
        soup = BeautifulSoup(response.content, 'html.parser')
    
        results = soup.find('div', class_="m-t nav-active-border b-primary").find_all('div', class_='box')
        for item in results:
            titles.append('**'+(item.find('h6').find('a').text)+'**')
            info.append(item.find('span', class_='text-muted').text)
        i+=1
    
    j=1
    while j<21:
        page1[j]=titles[j-1]+" ("+info[j-1]+")"
        j+=1
    rankings.append(page1)
    j=21
    while j<41:
        page2[j]=titles[j-1]+" ("+info[j-1]+")"
        j+=1
    rankings.append(page2)
    
    j=41
    while j<61:
        page3[j]=titles[j-1]+" ("+info[j-1]+")"
        j+=1
    rankings.append(page3)
    
    j=61
    while j<81:
        page4[j]=titles[j-1]+" ("+info[j-1]+")"
        j+=1
    rankings.append(page4)
    j=81
    while j<101:
        page5[j]=titles[j-1]+" ("+info[j-1]+")"
        j+=1
    rankings.append(page5)
    
    return rankings

def make_list(page={}):
    value =''
    i = int(list(page.keys())[0])
    while i<int(list(page.keys())[19])+1:
        value+= str(i)+". " + page[i] + '\n' + '\n'
        i+=1
    return value



    