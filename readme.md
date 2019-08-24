install reddis and start the server.
install from requirements.txt

Update settings to add your own mail id and password.
If you are using gmail, enable non secure app access on.

start django project by python manage.py runserver.

open postman and make a post api call to http://localhost:8000/api/sendEmails

body is json in following format : 

{
	"urls":["http://www.amazon.com","http://www.flipkart.com","http://www.youtube.com","http://www.facebook.com","http://www.instagram.com"],
	"email":"ayushpalakcs@gmail.com"
}

Note: URLs must be valid and start with http ot https.
      Maild id must be in this format:  something@something.some