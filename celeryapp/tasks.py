from __future__ import absolute_import, unicode_literals
from CeleryProject import settings
from celery import shared_task
from django.core.mail import EmailMessage
import requests
import zipfile


@shared_task
def sendEmailTask(urls=[], email=""):
    # getting url data and saving it as text file.
    try:
        for url in urls:
            res = requests.get(url)
            with open(url.split("://")[1]+".html", "w") as f:
                print("text writing")
                f.write(res.text)
    except Exception as e:
        print(str(e)+ "not able to connect to url.")
        return print("task failed")
    
    # zipping text files to a zip file.
    try:
        zf = zipfile.ZipFile('website_data.zip', mode='w')
        print('adding to zip')
        [zf.write(url.split("://")[1]+'.html') for url in urls]
        
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

