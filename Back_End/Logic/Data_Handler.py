import mysql.connector

class DataHandler():

    def __init__(self):
        """Object handling all the queries made by the program ,used to link the database to the program """
        pass
    def insertOneLink(self,data):
        """ Args : 
            data : Dict ; content formated by the return of a scraping function
        
        
         Add the furnished data to the table "links " 
        
        """
        
        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)


        client = local

        cursor = client.cursor()
        print(data["url"])

        request = "INSERT INTO links (article_id,link) VALUES(%s,'%s');"%(1,data["url"])
        print(request)
        cursor.execute(request)

        print("data Sent ; ",data)
        client.commit()
        cursor.close()
        client.close()


    def findLinks(self):
        """ Args : None 
        
        Find all the links present in the table links"
        
        """

        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)

        client = local # change to prod

        
        cursor = client.cursor()

        cursor.execute("SELECT * FROM links")

        document_list = []

        for link in cursor:
            document_list.append(link) 

        client.close()

        return document_list
    

    def insertOnePrice(self,data):
        """Args : 
            data : Dict 
        
         Add the furnished data to the table "price_tracker" 
         
         """
        print("data reçu dans le DataHandler",data )
        
        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)

        client = local # change to prod
        cursor = client.cursor()
  
        request = "INSERT INTO price_tracker (product_name,link,price) VALUES('%s','%s',%s);"%(data["title"],data["url"],data["price"])
        print(request)
        cursor.execute(request)

        print("data Sent ; ",data)
        client.commit()
        cursor.close()
        client.close()
    


    def findAlerts(self,id_article,current_price):
        """Args : 
            id_article : Int ; Id of the article updated 
            current_price : Int ; current price found for the product
        
        
        Find all concerned users for a tracked product , and call the function createAlerts() to return possible alerts to execute
        
        """
        
        #print("id_article reçu dans le DataHandler",id_article )        
        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)

        client = local # change to prod
        cursor = client.cursor()
  
        request = "SELECT * from article_user WHERE article_id = %s;"%(id_article)
        
        cursor.execute(request)
        results = cursor.fetchall()
     
        cursor.close()
        client.close()

        return self.createAlerts(results,current_price)



    def createAlerts(self,tab_of_alerts,current_price):
        """Args : 
            Tab_of_alerts : Tab ; list of users  
            current_price : Int ; current price found for the product
        
        
        For all concerned users given a tracked product, check if the price the threshold is met and in that case, 
        add a tuple to a list with all the information needed to contact them
        
        """
        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)

        client = local # change to prod
        list_to_notify = []
        
        for article in tab_of_alerts:
            
            if current_price <= article[3]:
                cursor_alert = client.cursor()
                request = "SELECT * from user WHERE id = %s;"%(article[1])
                cursor_alert.execute(request)
                person_to_alert = cursor_alert.fetchall()
                print(person_to_alert)
                list_to_notify.append((person_to_alert[0][1],person_to_alert[0][5],self.findArticleName(article[2]),current_price))
        
        return list_to_notify
    
    def findArticleName(self,id_article):
        """Args :
            Int : id_article ; id of a product
        
         Returns the name of a product given its ID  
         
         """

        local = mysql.connector.connect(
                        host="localhost",
                        user="admin",
                        password="LinodeTrackerWXCVBN",
                        database="PriceTracker",)

        client = local # change to prod
        cursor = client.cursor()
  
        request = "SELECT * from article WHERE id = %s;"%(id_article)
        
        cursor.execute(request)
        results = cursor.fetchall()
        
        cursor.close()
        client.close()

        return results[0][1]

    def findOnePrice(self,data):
        """Params : data ; Find the furnished data in the Table """
        print("data Sent ; ",data)
        self.client["price_tracker"]["price_tracker"].find_one(data)

    def findAll(self,data):
        pass
