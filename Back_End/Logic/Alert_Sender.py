import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

class AlertSender():

    def __init__(self):
        pass
    def sendTestMail(self):
        """ Args : None 
        
        Function to test if the module works correctly
        
        """
        self.mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        self.msg = MIMEMultipart()

        self.msg['From'] = 'none'
        self.msg['To'] = 'alexandre.pignard@outlook.fr'
        self.msg['Subject'] = 'Le sujet de mon mail' 
        self.message = 'Bonjour !'
        self.msg.attach(MIMEText(self.message))
        self.mailserver.starttls()
        self.mailserver.login('Myr724901@gmail.com', 'Myr7894561230&_')
        self.mailserver.sendmail('Myr724901@gmail.com', 'alexandre.pignard@outlook.fr', self.msg.as_string())
        self.mailserver.quit()

    def sendCustomMailAlert(self,recipient,article,current_price):
        """ Args : 
            recipient : String ; email adress string
            article :  String ; name of the product tracked
            current_price : Int ; current price for that product
        
        Function in charge of creating,formating and send an e-mail alert
        
        """
        self.mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        self.msg = MIMEMultipart()

        self.msg['From'] = 'none'
        self.msg['To'] = recipient
        self.msg['Subject'] = 'Prix atteint sur l\'article  :'+article
        self.message = 'Bonjour ! Votre '+article+" est actuellement à : "+ str(current_price)
        self.msg.attach(MIMEText(self.message))
        self.mailserver.starttls()
        self.mailserver.login('pricetrackerm1@gmail.com', 'kAWG36qT4b3kDMr')
        self.mailserver.sendmail('pricetrackerm1@gmail.com', recipient , self.msg.as_string())
        self.mailserver.quit()


    def sendCustomSMSAlert(self,phoneNumber,article,current_price):
        """ Args : 
            phoneNumber : String ; phone number adress string
            article :  String ; name of the product tracked
            current_price : Int ; current price for that product
        
        Function in charge of creating,formating and send an sms alert
        
        """
        if phoneNumber != None:
            client = boto3.client('sns',region_name="eu-west-3")
            client.publish(PhoneNumber="+33"+phoneNumber,Message="Bonjour ! Votre "+article+" est actuellement à : "+ str(current_price))

    def sendAlertsLoop(self,list_to_alert):
        """ Args : 
            list_to_alert : [Tuples] ; Tab of tuples of infos needed to create alerts

        
        Function going over every users who's product reached their wished threshold ,creating and sending customised alerts 
        
        """

        for alert in list_to_alert:
            print("mail to send to ",alert)
            self.sendCustomMailAlert(alert[0],alert[2],alert[3])
            self.sendCustomSMSAlert(alert[1],alert[2],alert[3])


