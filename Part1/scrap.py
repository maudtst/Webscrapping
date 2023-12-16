# Import Libraries
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import functools
import json
import time

class Restaurant:
    
    def __init__(self,card,resto,current_offset,page_num):
        self.card         = card
        self.res_cnt      = resto
        self.current_data = current_offset
        self.data_offset  = page_num
        
        self.scrape_title()
        self.scrape_url()           #self.url
        if self.url is not None:
            self.getInfos()         #self.info()  self.reviews

    def scrape_title(self):
        title = self.card.find_all("div", class_="RfBGI")
        self.title = None if len(title) < 1 else title[0].text

    def scrape_url(self):
        url_element = self.card.find('a', class_='Lwqic Cj b', href=True)
        if url_element:
            self.url = "https://www.tripadvisor.in/" + url_element['href']
        else:
            self.url=None
        
    def get_restaurant_soup(self):
        session = HTMLSession()
        response = session.get(self.url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def getInfos(self):
        soup = self.get_restaurant_soup()
        self.info = {
            "adress"        :Restaurant.scrape_adress(soup),
            "phone"         :Restaurant.scrape_phone(soup),
            "schedule"      :Restaurant.scrape_schedules(soup),
            "nb_reviews"    :Restaurant.scrape_Nbreview(soup),
            **Restaurant.scrape_ratings(soup),
            **Restaurant.scrape_details(soup),
        }
        self.reviews = Restaurant.scrape_reviews(soup)
            
    def scrape_adress(soup):
        address_element = soup.find("div", class_="kDZhm IdiaP")
        address = address_element.find("span", class_="yEWoV").get_text() if address_element else None
        return address

    def scrape_phone(soup):
        phone_element = soup.find("span", class_="AYHFM")
        phone = phone_element.get_text() if phone_element else None
        return phone

    def scrape_schedules(soup):
        # Pour obtenir les heures d'ouverture :
        hours_element = soup.find("span", class_="KscYp")
        hours = hours_element.get_text() if hours_element else None
        return hours

    def scrape_Nbreview(soup):
        soup       = soup.find("div", class_="vQlTa")
        if soup is None:
            return None
        nb_reviews = soup.find("span", class_="AfQtZ").text
        return nb_reviews

    def scrape_details(soup):
        soup    = soup.find("div",class_="UrHfr")
        if soup is None : return {"details":None}

        labels  = soup.find_all("div", class_="tbUiL b")
        details = soup.find_all("div", class_="SrqKb")

        if labels and details:
            labels  = [label.text+"_detail" for label in labels]
            details = [detail.text for detail in details]
            dico    = dict(zip(labels,details))
            return dico
        else :
             return {"details":None}

    def scrape_ratings(soup):
        soup    = soup.find("div",class_="hILIJ")
        if soup is None: return {"ratings":None}

        labels  = soup.find_all("span", class_="BPsyj")
        ratings = soup.find_all("span", class_="ui_bubble_rating")

        if labels and ratings:
            labels = ["global_rating"]+[label.text+"_rating" for label in labels]
            ratings = [int(rating["class"][1].replace('bubble_', ''))/10 for rating in ratings]
            dico = dict(zip(labels,ratings))
            return dico
        return {"ratings":None}

    def scrape_reviews(soup):
        #reviews title
        quotes = soup.findAll("div", class_="quote")
        #reviews entry
        reviews = soup.findAll("p", class_="partial_entry")
        if len(quotes)>0:
            quotes = [quote.text for quote in quotes]
            reviews = [review.text for review in reviews]
            return dict(zip(quotes,reviews))
        else:
            return {"reviews":None}
        
    def infosToDico(self):
        return {"name":self.title,"url":self.url,**self.info}
        
class RestaurantsCity:
    
    def __init__(self,scv):
        self.current_offset = scv["data_offset_lower_limit"]
        self.upp_offset  = scv["data_offset_upper_limit"]
        self.page_num    = scv["starting_page_num"]
        self.page_size   = scv["page_size"]
        self.geo_code    = scv["geo_code"]
        self.city        = scv["city_name"]
        self.restaurants,self.reviews = self.getRestaurantsCity()    
        
    def getRestaurantsCity(self):
        restaurants,reviews = [],[]
        while self.current_offset <= self.upp_offset:
            print(f"Scraping started for Page Number: {self.page_num} with Dataoffset: {self.current_offset}\n")
            soup = self.get_soup_content()
            page_restaurant,page_reviews = self.GetPageRestaurants(soup)
            restaurants += page_restaurant
            reviews     += page_reviews
            print(f"Scraping completed for Page Number: {self.page_num} with Dataoffset: {self.current_offset}\n")
            print(f"-------\n")
            self.page_num = self.page_num + 1
            self.current_offset = self.current_offset + 30
        return restaurants,reviews
    
    def GetPageRestaurants(self,soup):
        start = (self.page_num * self.page_size) + 1
        end   = start + self.page_size
        restaurant_list,reviews_list = [],[]
        for resto in range(start, end):
            card = RestaurantsCity.get_card(resto, soup)
            if card is None:
                break
            restaurant_data = Restaurant(card,resto,self.current_offset,self.page_num)
            restaurant_list.append(restaurant_data.infosToDico())
            reviews_list.append(restaurant_data.reviews)
        return restaurant_list,reviews_list
    
    def get_card(resto,soup):
        card_tag = f"{resto}_list_item"
        #print(f"Scraping item number: {card_tag}")
        card = soup.find("div", {"data-test": card_tag})
        return card   
        
    def get_soup_content(self):
        url = self.get_url()
        print("Starting html session\n")
        r = HTMLSession()
        response_obj = r.get(url, verify=False)
        soup_content = BeautifulSoup(response_obj.content, "html.parser")
        return soup_content
    
    def get_url(self):
        data_offset_var = "-oa" + str(self.current_offset)
        if  self.current_offset == 0:
            data_offset_var = ""
        url = f"https://www.tripadvisor.in/RestaurantSearch-g{self.geo_code}{data_offset_var}-a_date.2023__2D__03__2D__05-a_people.2-a_time.20%3A00%3A00-a_zur.2023__5F__03__5F__05-{self.city}.html#EATERY_LIST_CONTENTS"
        #url = f"https://www.tripadvisor.fr/RestaurantSearch-g{self.geo_code}{data_offset_var}-a_date.2023__2D__03__2D__05-a_people.2-a_time.20%3A00%3A00-a_zur.2023__5F__03__5F__05-{self.city}.html#EATERY_LIST_CONTENTS"
        print("URL to be scraped: ", url, "\n")
        return url

 
    def saveInfosCSV(self):
        print("\n______________________________________________________________________________________\n")
        print("storing the data in csv")
        output_df = pd.DataFrame(self.restaurants)
        #output_df.to_csv("restaurantsTripAdvisor.csv", index= False)
        print("csv not stored, please do it manually")
        return output_df
        
    def saveReviewsJson(self):
        print("\n______________________________________________________________________________________\n")
        print("storing reviews in json file")
        all_reviews = {}
        for i in range(len(self.reviews)):
            all_reviews[str(i)] = self.reviews[i]
        with open("reviewsTripAdvisor.json", "w") as json_file:
            json.dump(all_reviews, json_file)
        print("json file stored")
        return all_reviews
    
class Michelin:
    def __init__(self):
        self.url    = "https://guide.michelin.com"
        self.offset = 0
        self.step   = 20
        self.restaurants = self.getMichelinRestaurants()
        
    def getMichelinRestaurants(self):
        page = "/fr/fr/bretagne/vannes/restaurants/page/1"
        restaurants=[]
        while page is not None:
            print(f"Scraping started for page with Dataoffset: {self.offset}\n")
            soup = Michelin.getSoupContent(self.url+page)
            print("URL to be scraped: ", self.url+page, "\n")
            restaurants.extend(Michelin.getPageRestaurants(soup))
            print(f"Scraping completed for page with dataoffset: {self.offset}\n")
            print(f"-------\n")
            self.offset = self.offset+self.step
            page = Michelin.getNextPage(soup,self.offset)
        return restaurants
        
    def getSoupContent(url):
        r = HTMLSession()
        print("Starting html session\n")
        obj  = r.get(url, verify=False)
        soup = BeautifulSoup(obj.content, "html.parser")
        return soup
    
    def getNextPage(soup,offset):
        page = soup.find("a", {"offset": f"{offset}"})
        if page:
            return page.get("href")
        else:
            return None
    
    def getPageRestaurants(soup):
        cards = Michelin.getVannesCards(soup)
        infos = [Michelin.scrapInfo(card) for card in cards]
        return infos
    
    def getVannesCards(soup):
        cards = soup.findAll("div", class_ = "col-md-6 col-lg-4 col-xl-3")
        return Michelin.cardsInVannes(cards)  

    def cardsInVannes(cards):
        cities = [card.find("div", class_="love-icon pl-icon js-favorite-restaurant")["data-dtm-city"] for card in cards]
        cards  = [card for card,city in zip(cards,cities) if city == "Vannes"]
        return cards

    def scrapInfo(card):
        name    = card.find("h3", class_="card__menu-content--title").get_text(strip=True) 
        cuisine = card.find("div", class_="card__menu-footer--price").get_text(strip=True).split("·")[1].strip()
        chefs   = card.find_all(attrs={"data-dtm-chef": True})
        chefs   = [chef["data-dtm-chef"] for chef in chefs]
        distinctions = card.find_all(attrs={"data-dtm-distinction": True})
        distinctions = [distinction["data-dtm-distinction"] for distinction in distinctions]
        return name,chefs,cuisine,distinctions
    
    def saveInfosCSV(self):
        print("\n______________________________________________________________________________________\n")
        print("storing the data in csv")
        output_df = pd.DataFrame(self.restaurants, columns=['name', 'chef', 'cuisine', 'distinction'])
        output_df.to_csv("RestaurantsMichelin.csv", index= False)
        print("csv stored")
        return output_df
    

        

