class TemplateDefault():
    
    def __init__(self):
        """ Base init of the any template """
        self.baseUrl = ""
        self.finalUrl = ""


    def buildUrl(self,searchTerms):
        """ Build an url with fournished search terms """
        
        self.finalUrl += self.baseUrl
        for term in searchTerms:
            self.finalUrl += term + "+" 

        return self.finalUrl

    
    def scrapeFromUrl(self,searchUrl):
        """ Param : String; Return Dict  ; 
        
        Placeholder function for each template to implement their scraping methods
        
        returns None
        """        

        return None

    def scrapeTest(self,searchUrl,html):
        """ Param : String; Return Dict ; 
        
        Placeholder function for each template to implement their test scraping methods
        
        returns None
        """      
        return None 
