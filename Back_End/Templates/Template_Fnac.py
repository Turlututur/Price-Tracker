from inspect import currentframe
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import unicodedata
import json 



class TemplateFnac():
    """ Base Fnac query template """
    
    def __init__(self):
        """ Base init of the Fnac template """
        self.baseUrl = "https://www.amazon.fr/s?k="
        self.finalUrl = ""


    def buildUrl(self,searchTerms):
        """ Build an url with fournished search terms """
        
        self.finalUrl += self.baseUrl
        for term in searchTerms:
            self.finalUrl += term + "+" 

        return self.finalUrl

    def scrapeFromterms(self,searchTerms):
        """ Param : [String] ; Scrape with with the array terms furnished  """
        try:

            self.driver.get(self.buildUrl(searchTerms))

            self.html = self.driver.execute_script("return document.documentElement.outerHTML")
            self.soup = BeautifulSoup(self.html, 'html.parser')

            self.driver.quit()

            return self.soup

        except Exception as e:
            self.driver.quit()

        return "Exception met"



    def scrapeUsual(self):
        """ Param : None ; Scrape with the classic Fnac html  """
        info = []

        for title in self.soup.findAll("span",id="productTitle"):
            
            info.append(title.text)
                 
        price = self.soup.find("span", {"class":["a-price","a-text-price","a-size-medium"]})
                
            
        info.append(float(price.span.text.replace("€","").replace(",",".")))
                    
        info.append(datetime.timestamp(datetime.now()))

        return info

    
    def scrapeSpecialPatern_Book(self):
        """ Param : None ; Scrape with Fnac's book library html  """
        info = []
        print(self.html)
        for title in self.soup.findAll("h1",  {"class":["f-productHeader-Title"]},attrs={"data-automation-id":"product-title-label"}):
            info.append(title.text)
        print(info)
        for price in self.soup.findAll("span",  {"class":["f-priceBox-price","f-priceBox-price--reco", "checked"]}):
            info.append(float(unicodedata.normalize("NFKD", price.text).replace(" €","").replace(",",".")))
        
        print(info)

        price = self.soup.find("span", id="price")
        print(price.span)
        
        info.append(datetime.timestamp(datetime.now()))

        return info

    
    
    def scrapeFromUrl(self,searchUrl):
        """ Param : String; Return [JSON]  ; Scrape with the, hopefully, viable url given   """
        self.info = []

        try:
            # Options du crawler pour le faire tourner sans visu
            self.fireFoxOptions = Options()
            self.fireFoxOptions.add_argument("--headless")

            # Driver qui servira a crawl 
            self.driver = webdriver.Firefox(options=self.fireFoxOptions,executable_path='Templates/Ressources/geckodriver')
            self.driver.get(searchUrl)

            self.html = self.driver.execute_script("return document.documentElement.outerHTML")
            self.soup = BeautifulSoup(self.html, 'html.parser')

            self.driver.quit()

            try :
                info1 = self.scrapeUsual()
                self.info = info1
                return {"title": [self.info[0]] , "price": [self.info[1]] , "timestamp":[self.info[2]]}
            except Exception as e:
                print("Usual Form Failed")
                pass
    
            try:
                info2 = self.scrapeSpecialPatern_Book()
                self.info = info2
                return {"title": [self.info[0]] , "price": [self.info[1]] , "timestamp":[self.info[2]]}
            except:
                print("Unusual book form failed")



        except Exception as e:
            self.driver.quit()
            return e

        print(self.info)

        

        return None