# ReviewCode
Installation
$ pip install -r requirements.txt

Run Project
$ python manage.py runserver

Admin access
$ python manage.py createsuperuser
http://<project host:port>/admin

API
	list all api
	$ curl -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' 'http://127.0.0.1:8000/'
	create review
	$ curl -XPOST -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' -d '{
   	 "rating": 4,
   	 "title": "My first review",
   	 "summary": "This is my first review for this API",
   	 "company": {
       	 "name": "code",
       	 "description": "buster"
	    }
	 }' 'http://127.0.0.1:8000/review/'	
	list all reviews create by the user
	$ curl -H "Content-type: application/json" -H 'Authorization: Token <user token from admin>' 'http://127.0.0.1:8000/review/'
	[{
    "rating":5,
    "title":"My second review",
    "summary":"This is my second  review for this API",
    "ip_address":"127.0.0.1",
    "submission_date":"2020-07-01T11:31:11.322733Z",
    "company":{
        "name":"google",
        "description":"company"},
    "reviewer":{
        "user":{
            "username":"beket",
            "email":""},
    "key":<user token from admin>}}]
