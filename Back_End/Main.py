from Logic import Alert_Sender, Data_Handler,Scheduler,Scraper
from datetime import datetime


scraper = Scraper.Scraper()
dataHandler = Data_Handler.DataHandler()
alertSender =  Alert_Sender.AlertSender()
scheduler = Scheduler.Scheduler(scraper,dataHandler,alertSender)


scheduler.run()