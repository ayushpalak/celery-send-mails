from __future__ import absolute_import, unicode_literals
from CeleryProject import settings
from celery import shared_task
from django.core.mail import EmailMessage
import requests,re
import zipfile,copy

def isValidUrl(url):
    x = re.search("(http://|https://)www\.[a-zA-Z]{1,}\.[a-zA-Z]{1,}",url)
    if x:
        return True
    else:
        return False

@shared_task
def sendEmailTask(urls=[], email=""):
    # getting url data and saving it as text file.
    cleaned_urls = []
    for url in urls:
        if(isValidUrl(url)):
            try:
                res = requests.get(url)
                if(res.status_code == 200):
                    cleaned_urls.append(url)    
                    with open("downloaded_urls/"+url.split("://")[1]+".html", "w") as f:
                        print("text writing")
                        f.write(res.text)
            except Exception as e:
                print(e)
    print (cleaned_urls)
    # zipping text files to a zip file.
    try:
        zf = zipfile.ZipFile('downloaded_urls/website_data.zip', mode='w')
        print('adding to zip')
        [zf.write("downloaded_urls/"+url.split("://")[1]+'.html') for url in cleaned_urls]
        
        # sending mail using google SMTP
        try:
            email = EmailMessage(
                subject='Hello '+email,
                body='Please find the zip file attached in mail.',
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            email.attach_file("website_data.zip")
            email.send()
        except Exception as e:
            print(str(e)+ "unable to send mail.")
    except Exception as e:
        print(str(e)+ "unable to zip")
        return print("task failed")
    finally:
        print('closing')
        zf.close()

    return "mail sent successfully."

