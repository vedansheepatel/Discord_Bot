import requests
from bs4 import BeautifulSoup


def search_drama(user_message):
	search_terms = user_message.split()[1:]
	key_terms = '+'.join(search_terms)
	search_word = ' '.join(search_terms)
	
	response = requests.get('https://mydramalist.com/search?q='+key_terms)
	soup = BeautifulSoup(response.content, 'html.parser')

	result_links = soup.find('div', class_='col-lg-8 col-md-8').find_all('div', class_='box')

		#various cases
		#only one result (a movie or drama), multiple results (movies and dramas)
		#for now assume the top result is taken
		#future - ask for drama or movie specification when searching
		
	link = result_links[0]
	drama_url = (('https://mydramalist.com/') + link.find("h6").find('a')['href'])
    
	return drama_url

def get_data(drama_url):
    response = requests.get(drama_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    drama_info={}
    
    #get drama synopsis 
    drama_info["summary"] = soup.find("div", class_="show-synopsis").find("span").text.replace("\n"," ")
    mainbox = soup.find("div", class_="col-lg-8 col-md-8 col-rightx").find('div', class_='box-body')
    drama_info['poster'] = mainbox.find("img", class_="img-responsive")['src']
    drama_info['score'] = soup.find("div", class_="box deep-orange").text
    #fetch information under detail section on MDL
    additional_info = soup.find("div", class_="box-body light-b").find_all("li")
    #go through list in html to get details
    for item in additional_info:
        key= item.text.split(":")[0].lower()
        drama_info[key] = item.text.split(":")[1].strip()

    #get genre tags
    detailed_info = mainbox.find("div", class_="show-detailsxss").find("ul").find_all("li")
    for item in detailed_info:
                field = item.find('b').text.lower().rstrip(':')
                if field == 'genres':
                    all_info = ""
                    for i in item.find_all('a'):
                        all_info += i.text + ", "
                    all_info = all_info.rstrip(', ').strip()
                    if all_info != '':
                        drama_info['genres'] = all_info

    
    return drama_info

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
   
