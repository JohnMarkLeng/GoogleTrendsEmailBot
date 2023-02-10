import smtplib
import ssl
from email.message import EmailMessage
from datetime import date 
import requests
import schedule
from email.mime.text import MIMEText
import time

#Email python: https://towardsdatascience.com/how-to-easily-automate-emails-with-python-8b476045c151





def getGoogleTrendsNews(): 
    try:
        USTechUrl = 'http://localhost:3001/realTimeTrends/US/t'
        USBusinessUrl = 'http://localhost:3001/realTimeTrends/US/b'
        USTopStoriesUrl = 'http://localhost:3001/realTimeTrends/US/h'


        USTechData =  requests.get(url = USTechUrl).json()
        USBusinessData = requests.get(url = USBusinessUrl).json()
        USTopStoriesData = requests.get(url = USTopStoriesUrl).json()

        return USTechData, USBusinessData, USTopStoriesData

    except Exception as e:
        print(e)


def mail():
    
    #Get News
    USTechData, USBusinessData, UsTopStoriesData = getGoogleTrendsNews()

    body = """

    """

    email_sender = 'GooogleTrendsBot@gmail.com'
    email_password = ''             #####Dont Leak This Pass!!!######!!!!!
    email_receiver = 'gooogletrendsbot@gmail.com'

    today = date.today()
    formattedDate = today.strftime('%d %b %Y')
    # print(formattedDate)


    subject = f'{formattedDate} Google Trends Update'


    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    context = ssl.create_default_context()


    #Email Body Generation
    if len(USBusinessData) != 0:
        body = body + "<br><br><H1><b>US Business News: </b></H1><br>"
        # print(USTechData)
        for topic in USBusinessData:
            # print(topic)
            body += '<b>'
            for title in topic['EntityNames']:
                body = body + title + ", "
            body = body.rstrip(', ')
            body = body + "</b> <br>"
            for i in range(0, len(topic['ArticlesAndUrls'])):
                article = topic['ArticlesAndUrls'][i]
                url = article['Url']
                title = article['Title']
                body = body + f'<a href="{url}">{title}</a>' + '<br>'
                if i == 2:
                    break

    if len(UsTopStoriesData) != 0:
        body = body + "<br><br><H1><b>US Top Stories News: </b></H1><br>"
        # print(USTechData)
        for topic in UsTopStoriesData:
            # print(topic)
            body += '<b>'
            for title in topic['EntityNames']:
                body = body + title + ", "
            body = body.rstrip(', ')
            body = body + "</b> <br>"
            for i in range(0, len(topic['ArticlesAndUrls'])):
                article = topic['ArticlesAndUrls'][i]
                url = article['Url']
                title = article['Title']
                body = body + f'<a href="{url}">{title}</a>' + '<br>'
                if i == 2:
                    break


    if len(USTechData) != 0:
        body = body + "<br><H1><b>US Tech News: </b></H1><br>"
        # print(USTechData)
        for topic in USTechData:
            # print(topic)
            body += '<b>'
            for title in topic['EntityNames']:
                body = body + title + ", "
            body = body.rstrip(', ')
            body = body + "</b> <br>"
            for i in range(0, len(topic['ArticlesAndUrls'])):
                article = topic['ArticlesAndUrls'][i]
                url = article['Url']
                title = article['Title']
                body = body + f'<a href="{url}">{title}</a>' + '<br>'
                if i == 2:
                    break


    #use this to embed html
    body = MIMEText(body ,'html')
    em.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print("Email sent")

schedule.every().day.at("11:00").do(mail)


while True:
    schedule.run_pending()
    time.sleep(1)
    print("running")