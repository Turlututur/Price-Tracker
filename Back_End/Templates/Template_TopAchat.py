import imp
from Templates.Template_Default import TemplateDefault
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from datetime import datetime
import unicodedata
import json 


class TemplateTopAchat(TemplateDefault):
    """ Base Fnac query template """
    
    def __init__(self):
        """ Base init of the TopAchat template """
        self.baseUrl = "https://www.amazon.fr/s?k="
        self.finalUrl = ""
    
    def scrapeRawHtml(self,url):
        """ Args : Url : String ; Url to crawl 
        
        Scrape the html of a webpage then returns it "
        
            return : String
        """
        self.info = []
        self.fireFoxOptions = Options()
        self.fireFoxOptions.add_argument("--headless")

        # Driver qui servira a crawl 
        self.driver = webdriver.Firefox(options=self.fireFoxOptions,executable_path=GeckoDriverManager().install())
        self.driver.get(url)

        self.html = self.driver.execute_script("return document.documentElement.outerHTML")
        return self.html

    def scrapeTest(self,searchUrl,html):
        """ Args: searchUrl: String ; Url of the webpage scraped
                  html : String ; Html of said webpage      
        
        Function Used to work with UnitTests; ignore the scraping process focus on the the information extraction
        
        returns [String,Float,DateTime] 
        """

        self.soup = BeautifulSoup(html, 'html.parser')

        try :
            info1 = self.scrapeUsual()
            self.info = info1
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("Usual Form Failed")
            

    def scrapeFromUrl(self,searchUrl):
        """ Param : String; Return [JSON]  ; Scrape with the, hopefully, viable url given   """
        self.info = []
        self.fireFoxOptions = Options()
        self.fireFoxOptions.add_argument("--headless")

        # Driver qui servira a crawl 
        self.driver = webdriver.Firefox(options=self.fireFoxOptions,executable_path=GeckoDriverManager().install())
        self.driver.get(searchUrl)

        self.html = self.driver.execute_script("return document.documentElement.outerHTML")
        self.soup = BeautifulSoup(self.html, 'html.parser')
        
        try:
            # Options du crawler pour le faire tourner sans visu

            self.request = self.driver.get(searchUrl)
            self.request.html.render()
            self.html = self.request.text
            self.soup = BeautifulSoup(self.html, 'html.parser')

            try :
                info1 = self.scrapeUsual()
                self.info = info1
                print("Info",self.info)
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl}
            except Exception as e:
                print("Usual Form Failed",e)
                pass
    
            try:
                info2 = self.scrapeSpecialPatern_Book()
                self.info = info2
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl}
            except:
                print("Unusual book form failed")

        except Exception as e:
	       
            return e

        print(self.info)
        return None

    def scrapeUsual(self):
        """ Param : None ; Scrape with the classic TopAchat html  """
        info = []

        title = self.soup.find("h1",{"class":["fn"]})
        
        info.append(title.text)
                 
        price  = self.soup.find("span",  {"class":["priceFinal"]})

        info.append(float(unicodedata.normalize("NFKD", price.text).replace(" €","").replace(",",".")))
                
                    
        info.append(datetime.timestamp(datetime.now()))
        print("Infos extraites  :", info)
        return info

    
    def scrapeSpecialPatern_Book(self):
        pass

    
    

