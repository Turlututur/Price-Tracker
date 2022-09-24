from turtle import ht
from Templates import Template_Amazon,Template_Fnac,Template_TopAchat


class Scraper():
    def __init__(self):
        """ Initialisation of the Scraper object"""
    
        self.availableTemplate = {"https://www.amazon.fr/":Template_Amazon.TemplateAmazon(),
                                  "https://www.topachat.com/":Template_TopAchat.TemplateTopAchat()}

    def adaptTemplateFromUrl(self,url):
        """ 
         Args : Url    :String  
        
        Find the correct template based on the URL Domain name and returns the scraping function associated
        
        """
        for domain,template in self.availableTemplate.items():
            
            if domain in url:
                return template
        pass


    def scrapeFromUrl(self,searchUrl):
        """ Args : searchUrl : String  
        
        Ask the current template to scrape the url given  
        
        """
        return self.adaptTemplateFromUrl(searchUrl).scrapeFromUrl(searchUrl)

    def scrapeRawHtml(self,searchUrl):
        """ Args : searchUrl : String  
        
        Ask the current template to scrape the raw html of the page  
        
        return String
        """

        return self.adaptTemplateFromUrl(searchUrl).scrapeRawHtml(searchUrl)

    def scrapeTest(self,searchUrl,html):

        """ Args : searchUrl : String ; url of the test  
                   html : String ; html to test

        Ask the current template to scrapeTest the furnished html  
        
        return [String,Float,DateTime]
        """
        return self.adaptTemplateFromUrl(searchUrl).scrapeTest(searchUrl,html)


