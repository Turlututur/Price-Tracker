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




class TemplateAmazon(TemplateDefault):
    
    def __init__(self):
        """ Base init of the Amazon template """
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

    def scrapeUsual(self):
        """ Args: None ; 
        
        Scrape with the classic Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []

        for title in self.soup.findAll("span",id="productTitle"):
            
            info.append(title.text)
                 
        price = self.soup.find("span", {"class":["a-price","a-text-price","a-size-medium"]})
                
            
        info.append(float(price.span.text.replace("€","").replace(",",".")))
                    
        info.append(datetime.timestamp(datetime.now()))


        return info

    
    def scrapeSpecialPatern_Book(self):
        """ Args: None ; 
        
        Scrape with a special Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []
        
        for title in self.soup.findAll("span",  {"class":["a-size-extra-large"]},id="productTitle"):
            info.append(title.text)

        for price in self.soup.findAll("span",id="price"):
            
            info.append(float(unicodedata.normalize("NFKD", price.text).replace(" €","").replace(",",".")))
        

        price = self.soup.find("span", id="price")

        
        info.append(datetime.timestamp(datetime.now()))

        return info
    


        
    def scrapeSpecialPatern_MultiChoiceBook(self):
        """ Args: None ; 
        
        Scrape with a special Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []
        
        for title in self.soup.findAll("span",id="productTitle"):
            info.append(title.text)

        for price in self.soup.findAll("span",  {"class":["a-price","a-text-price", "header-price"," a-size-base", "a-text-normal"]}):
            prix = [el.text for el in price]
            
            try:
                info.append(float(unicodedata.normalize("NFKD", price.text).replace("€","").replace(",",".")))
            except Exception as e :
                pass
            try:
                info.append(float(unicodedata.normalize("NFKD", price.text).replace(" €","").replace(",",".")))
            except Exception as e :
                pass
        
        info.append(datetime.timestamp(datetime.now()))

        return info

    def scrapeSpecialPatern_Outdoors(self):
        """ Args: None ; 
        
        Scrape with a special Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []
        for title in self.soup.findAll("span", id="productTitle"):
            info.append(title.text)

        for span in self.soup.find("span",{"class":["a-offscreen"]}):
            print(span)
            try:
                info.append(float(unicodedata.normalize("NFKD", span.text).replace("€","").replace(",",".")))
            except Exception as e :
                pass
            try:
                info.append(float(unicodedata.normalize("NFKD", span.text).replace(" €","").replace(",",".")))
            except Exception as e :
                pass

        info.append(datetime.timestamp(datetime.now()))

        return info

    def scrapeSpecialPatern_BoxedPrice(self):
        """ Args: None ; 
        
        Scrape with a special Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []
        for title in self.soup.findAll("span", id="productTitle"):
            info.append(title.text)

            for span in self.soup.find("span",{"class":["a-offscreen"]}):
                print(span)
                try:
                    info.append(float(unicodedata.normalize("NFKD", span.text).replace("€","").replace(",",".")))
                except Exception as e :
                    pass
                try:
                    info.append(float(unicodedata.normalize("NFKD", span.text).replace(" €","").replace(",",".")))
                except Exception as e :
                    pass

        info.append(datetime.timestamp(datetime.now()))

        return info


    def scrapeSpecialPatern_Occasion(self):
        """ Args: None ; 
        
        Scrape with a special Amazon html 
        
        returns [String,Float,DateTime] 
        """
        info = []
        
        for title in self.soup.findAll("span",id="productTitle"):
            info.append(title.text)

        for price in self.soup.findAll("span",  {"class":["a-size-base", "a-color-price", "offer-price", "a-text-normal"]}):
            for prix in self.soup.findAll("span",{"class":["a-price", "aok-align-center"]}):
                #print(prix.text)
                try:
                    info.append(float(unicodedata.normalize("NFKD", prix[-1]).replace("€","").replace(",",".")))
                except Exception as e :
                    pass
                try:
                    info.append(float(unicodedata.normalize("NFKD", prix[-1]).replace(" €","").replace(",",".")))
                except Exception as e :
                    pass
        
        info.append(datetime.timestamp(datetime.now()))

        return info
    
    
    def scrapeTest(self,searchUrl,html):
        """ Args: searchUrl: String ; Url of the webpage scraped
                  html : String ; Html of said webpage      
        
        Function to work with UnitTests; ignore the scraping process focus on the the information extraction
        
        returns [String,Float,DateTime] 
        """

        self.soup = BeautifulSoup(html, 'html.parser')

        try :
            info1 = self.scrapeUsual()
            self.info = info1
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("Usual Form Failed")
            
    
        try:
            info2 = self.scrapeSpecialPatern_Book()
            self.info = info2
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("Unusual book form failed")
            

        try:
            info3 = self.scrapeSpecialPatern_Occasion()
            self.info = info3
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("Unusual Occasion form failed")
            
        try:
            info4 = self.scrapeSpecialPatern_MultiChoiceBook()
            self.info = info4
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("MultiChoiceBook form failed")
            
        try:
            info5 = self.scrapeSpecialPatern_Outdoors()
            self.info = info5
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("Outdoors form failed")

        try:
            info5 = self.scrapeSpecialPatern_BoxedPrice()
            self.info = info5
            return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
        except Exception as e:
            print("BoxedPrice form failed")

    
    def scrapeFromUrl(self,searchUrl):
        """ Args: searchUrl: String ; Url of the webpage to scrape  
        
        Function Used into the main program to extract a viable information list from the webpage 
        
        returns [String,Float,DateTime] 
        """
        self.info = []
        self.fireFoxOptions = Options()
        self.fireFoxOptions.add_argument("--headless")

        # Driver qui servira a crawl 
        self.driver = webdriver.Firefox(options=self.fireFoxOptions,executable_path=GeckoDriverManager().install())
        self.driver.get(searchUrl)

        self.html = self.driver.execute_script("return document.documentElement.outerHTML")
        self.soup = BeautifulSoup(self.html, 'html.parser')
        try:
          
           
            self.driver.get(searchUrl)

            self.html = self.driver.execute_script("return document.documentElement.outerHTML")
            self.soup = BeautifulSoup(self.html, 'html.parser')

            self.driver.quit()

            try :
                info1 = self.scrapeUsual()
                self.info = info1
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except Exception as e:
                print("Usual Form Failed")
                pass
    
            try:
                info2 = self.scrapeSpecialPatern_Book()
                self.info = info2
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except:
                print("Unusual book form failed")
                pass

            try:
                info3 = self.scrapeSpecialPatern_Occasion()
                self.info = info3
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except:
                print("Unusual Occasion form failed")
            try:
                info4 = self.scrapeSpecialPatern_MultiChoiceBook()
                self.info = info4
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except Exception as e:
                print("MultiChoiceBook form failed")
            
            try:
                info5 = self.scrapeSpecialPatern_Outdoors()
                self.info = info5
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except Exception as e:
                print("Outdoors form failed")

            try:
                info5 = self.scrapeSpecialPatern_BoxedPrice()
                self.info = info5
                return {"title": self.info[0] , "price": self.info[1] , "timestamp":self.info[2],"url":searchUrl }
            except Exception as e:
                print("BoxedPrice form failed")

        except Exception as e:
            self.driver.quit()
            return e

        print(self.info)

        

        return None

