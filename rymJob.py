from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from random import randint
def get_header_list():
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + "d3cef6c6-025b-43b1-8bd7-fc38aa490c88")
    json_response = response.json()
    return json_response.get('result', [])

def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]

header_list = get_header_list()
#ua = UserAgent()
#header = {"User-Agent": str(ua.firefox)}
#driver = webdriver.Firefox()
artist = input('Enter artist name here, all lowercase with "-" for spaces:')
new_artist_string = artist.lower()
final_artist_string = new_artist_string.replace(' ', '-')
url = "https://rateyourmusic.com/artist/"
artistURL = url + final_artist_string
page = requests.get(artistURL, headers=get_random_header(header_list))
#driver.get(artistURL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="disco_type_s")
albums = results.find_all("div", class_="disco_release")
title_list = []
avg_rating_list = []
for album in albums:
    #print(album.text.strip())
    title = album.find("a", class_="album")
    avg_rating = album.find("div", class_="disco_avg_rating enough_data")
    your_rating = album.find("span", class_="disco_cat")
    if avg_rating is not None and title is not None:
        title_list.append(title.text.strip())
        avg_rating_list.append(avg_rating.text.strip())
        print(title.text.strip() + " || " + avg_rating.text.strip() + " || " )
    #print(your_rating)
max_len_string = max(title_list, key=len)
print("max length string = " + max_len_string)
max_len = len(max_len_string)

#max_len += 2
title_rating_dict = {title_list[i]: avg_rating_list[i] for i in range(len(title_list))}
for i in title_rating_dict:
    if i != max_len_string:
        print(i, title_rating_dict[i].rjust(max_len - len(i) + 5, ' '))
    else:
        print(i, ' ' +title_rating_dict[i])
    
    
#print(results.text.strip())
