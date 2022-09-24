from logging import exception
from typing import Type
import sched, time
from Logic.Data_Handler import DataHandler
from Logic.Scraper import Scraper
from Logic.Alert_Sender import AlertSender


class Scheduler():
    """
        Args : scraper     :Type[Scraper]
               dataHandler :Type[DataHandler]
               alertSender  :Type[AlertSender]
    
    
     Class responsible for the scheduling and overall behaviour of the program 
    
    """    
    def __init__(self,scraper:Type[Scraper],dataHandler:Type[DataHandler],alertSender:Type[AlertSender] ):

        
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.dataHandler = dataHandler
        self.scraper = scraper 
        self.alertSender = alertSender

        self.currentCrawledLinks = []


    def run(self):
        """ 
        Args : None
        
        Adds every links present in the database of links to crawl to the currentCrawledLinks list,adds a jobs 
    with the corresponding caracteristics found and triggers the scheduler run() function lauching the reccurent crawls,
    -- will stop if its job queue is empty --

        """
        for link in self.dataHandler.findLinks():
            print(link) 
            self.planReccurentCrawl(43200,link[2],link[1])
            self.currentCrawledLinks.append(link[2])

        self.checkForNewLinksToCrawl()
        self.scheduler.run()


    def planReccurentCrawl(self,delay,url,id_article):
        """ 
    Args : Delay        int (in seconds)
           Url          string
           id_article   Int
        
        Plan a recurent crawl of a specified page at a specified recurring time interval
        
        """
        
        self.scheduler.enter(delay,1,self.crawlAndSave,argument=[delay,url,id_article])
        print("Planned a Crawl : Delay ",delay," Seconds")
        print("Current Job List : ",self.scheduler.queue)
    

    def crawlAndSave(self,delay,url,id_article):
        """ 
    Args : Delay        Int (in seconds)
           Url          String
           id_article   Int
        
        If the conditions aren't met plan a new crawl at the original interval, otherwise send an email alert 

        """        
        
        document = self.scraper.scrapeFromUrl(url)
        print("Document Transmit : ",document)

        if document != None:
            try:
                # Try and catch to get all the possible fail states in to the logs
                document["id_article"] = id_article
        
                print("Alerts : ",id_article)
        

        
                self.planReccurentCrawl(delay,url,id_article)
                self.dataHandler.insertOnePrice(document)
                print("Crawled and Saved : ",document)
                self.alertSender.sendAlertsLoop(self.dataHandler.findAlerts(id_article,document["price"]))
            except exception as e:
                print(e)
        else:
            pass


    def checkForNewLinksToCrawl(self):
        """ 
    Args : None
        
        Lookup in the link the database if any new links to track were inserted, and if so, add them to the currently tracked links and create a delayed crawl for it
        
        """

        print("Chechking for new links to Crawl")
        for link in self.dataHandler.findLinks():
            if link[2] not in self.currentCrawledLinks:
                self.planReccurentCrawl(3600,link[2],link[1])
                self.currentCrawledLinks.append(link[2])
        
        self.scheduler.enter(3600,1,self.checkForNewLinksToCrawl)



    
        
