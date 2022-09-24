from cgitb import html
import pickle
from Logic.Scraper import Scraper

class UnitTester():

    def __init__(self) -> None:
        """ Args : None  
        
        Initialisation of the UnitTester
        
        return UnitTester
        """
        self.scraper = Scraper() 
    
    def createEmptyFile(self):
        """ Args : None  
        
        Create an empty UnitTests file for the program to use 
        
        return None
        """
        pickle.dump({}, open('UnitTests.pkl', 'wb'))

    def addToTests(self,url,expectedPrice):
        """ Args : url : String ; Url to crawl to get the wished html to test
                   expectedPrice :  Float ; Expected price to be scraped  

        Fetch the given url raw html and stock it with the expected price into the uniTests file 
        
        return None
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        self.tests[url] = {"html":self.scraper.scrapeRawHtml(url),"price":expectedPrice}
        pickle.dump(self.tests, open('UnitTests.pkl', 'wb'))
    
    def removeFromTests(self,url):

        """ Args : url : String ; Url to delete from tests

        Delete the given url from the unitTests file
        
        return None
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        del self.tests[url]
        pickle.dump(self.tests, open('UnitTests.pkl', 'wb'))

    def printTests(self):
        """ Args : None

        Show all the tests in the uniTests file 
        
        return None
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        for key,value in self.tests.items():
            print(key)
    
    def getTestHtml(self,url):
        """ Args : url : String ; Url key to get the corresponding stocked html 

        Get the current stocked html for a given url key
        
        return String
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        html_test = self.tests[url]["html"]
        pickle.dump(self.tests, open('UnitTests.pkl', 'wb'))
        return html_test
    
    def getAllTests(self):
        """ Args : None

        Return a copy of the current unitTests file
        
        return Dict
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        allTests = self.tests
        pickle.dump(self.tests, open('UnitTests.pkl', 'wb'))
        return allTests
    
    def changeTestPriceCondition(self,url,newPrice):
        """ Args : url : String ; Url of the condition price change
                   newPrice : Float ; new price condition to replace the old one

        Change the price condition of test
        
        return None
        """
        self.tests = pickle.load(open('UnitTests.pkl', 'rb'))
        self.tests[url]["price"] = newPrice
        pickle.dump(self.tests, open('UnitTests.pkl', 'wb'))

    def testTemplate(self,url,html):
        """ Args : url : String ; Url of the html tested
                   html : String ; Html to test

        Test the current html with the scrapeTest function of the template 
        
        return None
        """
        
        return self.scraper.scrapeTest(url,html)


    def runAllTests(self):

        """ Args : None

        Run all the tests available the the unitTests file 
        
        return None
        """
        for url,data in self.getAllTests().items():

            test = self.testTemplate(url,data["html"])
            if test == None:
                print("Test ",url," ------Massively Failed------")

            elif data["price"] == test["price"]:
                print("Test : ",test["title"]," ------Passed------ ","Price : ",test["price"])

            else:
                print("Test : ",test["title"]," ------Failed------ ")

        return None